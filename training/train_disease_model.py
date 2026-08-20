import argparse
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def build_loaders(data_dir, batch_size):
    train_transform = transforms.Compose(
        [
            transforms.Resize((256, 256)),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(20),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    val_transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    train_data = datasets.ImageFolder(Path(data_dir) / "train", transform=train_transform)
    val_data = datasets.ImageFolder(Path(data_dir) / "val", transform=val_transform)
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False, num_workers=2)
    return train_loader, val_loader, train_data.classes


def build_model(num_classes):
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            total += labels.size(0)

    return total_loss / total, correct / total


def train(args):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_loader, val_loader, class_names = build_loaders(args.data_dir, args.batch_size)
    model = build_model(len(class_names)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.3)

    best_accuracy = 0.0
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(args.epochs):
        model.train()
        running_loss = 0.0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)

        scheduler.step()
        train_loss = running_loss / len(train_loader.dataset)
        val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)
        print(f"epoch={epoch + 1} train_loss={train_loss:.4f} val_loss={val_loss:.4f} val_acc={val_accuracy:.4f}")

        if val_accuracy > best_accuracy:
            best_accuracy = val_accuracy
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "class_names": class_names,
                    "model_version": "resnet18-plant-disease-v1",
                    "validation_accuracy": best_accuracy,
                },
                output_path,
            )

    print(f"saved best model to {output_path} with accuracy {best_accuracy:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ResNet18 plant disease classifier.")
    parser.add_argument("--data-dir", default="data/plant_disease", help="Dataset folder with train/ and val/ subfolders.")
    parser.add_argument("--output", default="models/plant_disease_resnet18.pth")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    train(parser.parse_args())
