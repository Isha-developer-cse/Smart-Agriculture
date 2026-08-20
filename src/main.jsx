import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  BarChart3,
  CloudSun,
  FlaskConical,
  Languages,
  Leaf,
  LogIn,
  Menu,
  Upload,
  X
} from "lucide-react";

import { api } from "./api/client";
import { translations } from "./i18n/translations";
import "./index.css";

const AppContext = createContext(null);

const routes = [
  { path: "/", labelKey: "dashboard", icon: BarChart3 },
  { path: "/disease", labelKey: "detect", icon: Leaf },
  { path: "/crop", labelKey: "crop", icon: Activity },
  { path: "/fertilizer", labelKey: "fertilizer", icon: FlaskConical },
  { path: "/weather", labelKey: "weather", icon: CloudSun },
  { path: "/login", label: "Login", icon: LogIn }
];

function App() {
  const [path, setPath] = useState(window.location.pathname);
  const [language, setLanguage] = useState("en");

  useEffect(() => {
    const onPopState = () => setPath(window.location.pathname);
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  function navigate(nextPath) {
    window.history.pushState({}, "", nextPath);
    setPath(nextPath);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const value = useMemo(() => ({ language, setLanguage, t: translations[language], path, navigate }), [language, path]);

  return (
    <AppContext.Provider value={value}>
      <Layout>
        <Router path={path} />
      </Layout>
    </AppContext.Provider>
  );
}

function Router({ path }) {
  switch (path) {
    case "/":
      return <DashboardPage />;
    case "/disease":
      return <DiseasePage />;
    case "/crop":
      return <CropPage />;
    case "/fertilizer":
      return <FertilizerPage />;
    case "/weather":
      return <WeatherPage />;
    case "/login":
      return <LoginPage />;
    default:
      return <NotFoundPage />;
  }
}

function Layout({ children }) {
  const { language, setLanguage, t, path, navigate } = useApp();
  const [mobileOpen, setMobileOpen] = useState(false);

  const nav = (
    <nav className="flex flex-col gap-2 lg:flex-row lg:items-center">
      {routes.map((route) => {
        const Icon = route.icon;
        const active = route.path === path;
        return (
          <button
            key={route.path}
            onClick={() => {
              navigate(route.path);
              setMobileOpen(false);
            }}
            className={`nav-link ${active ? "nav-link-active" : ""}`}
          >
            <Icon className="h-4 w-4" />
            {route.label || t[route.labelKey]}
          </button>
        );
      })}
    </nav>
  );

  return (
    <div className="min-h-screen text-agro-ink">
      <header className="sticky top-0 z-20 border-b border-black/10 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-4">
          <button className="flex items-center gap-3 text-left" onClick={() => navigate("/")}>
            <div className="grid h-11 w-11 place-items-center rounded-lg bg-agro-green font-black text-white">AG</div>
            <div>
              <h1 className="text-xl font-black">AgroCrop AI</h1>
              <p className="text-xs text-slate-500">React · Flask · PyTorch · OpenCV</p>
            </div>
          </button>

          <div className="hidden lg:block">{nav}</div>

          <div className="flex items-center gap-2">
            <Languages className="h-4 w-4 text-agro-green" />
            <select className="input w-32" value={language} onChange={(event) => setLanguage(event.target.value)}>
              <option value="en">English</option>
              <option value="hi">हिन्दी</option>
            </select>
            <button className="btn-secondary px-3 lg:hidden" onClick={() => setMobileOpen(true)}>
              <Menu className="h-4 w-4" />
            </button>
          </div>
        </div>
      </header>

      {mobileOpen && (
        <div className="fixed inset-0 z-30 bg-black/40 lg:hidden">
          <aside className="ml-auto h-full w-80 bg-white p-5 shadow-xl">
            <div className="mb-5 flex items-center justify-between">
              <strong>Menu</strong>
              <button className="btn-secondary px-3" onClick={() => setMobileOpen(false)}>
                <X className="h-4 w-4" />
              </button>
            </div>
            {nav}
          </aside>
        </div>
      )}

      <main className="mx-auto max-w-7xl px-5 py-8">{children}</main>
    </div>
  );
}

function DashboardPage() {
  const { t, navigate } = useApp();
  const cards = [
    { label: t.detect, icon: Leaf, path: "/disease", copy: "Upload leaf images and classify crop diseases." },
    { label: t.crop, icon: Activity, path: "/crop", copy: "Recommend crops from soil and climate values." },
    { label: t.fertilizer, icon: FlaskConical, path: "/fertilizer", copy: "Find nutrient gaps and fertilizer guidance." },
    { label: t.weather, icon: CloudSun, path: "/weather", copy: "Fetch live climate conditions for your farm." }
  ];

  return (
    <>
      <section className="mb-6 overflow-hidden rounded-lg bg-[linear-gradient(90deg,rgba(18,58,36,.95),rgba(18,58,36,.62)),url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1800&q=80')] bg-cover bg-center p-8 text-white md:p-14">
        <p className="mb-3 inline-flex rounded-full bg-white/15 px-3 py-1 text-xs font-bold">Full-stack AI agriculture system</p>
        <h2 className="max-w-3xl text-4xl font-black leading-tight md:text-6xl">{t.title}</h2>
        <p className="mt-4 max-w-2xl text-white/80">{t.subtitle}</p>
        <div className="mt-6 flex flex-wrap gap-3">
          <button className="btn-primary bg-white text-agro-green hover:bg-agro-mint" onClick={() => navigate("/disease")}>Start diagnosis</button>
          <button className="btn-secondary border-white/30 bg-white/10 text-white hover:bg-white/20" onClick={() => navigate("/crop")}>Recommend crop</button>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <button className="panel text-left transition hover:-translate-y-1 hover:shadow-lg" key={card.path} onClick={() => navigate(card.path)}>
              <Icon className="mb-4 h-8 w-8 text-agro-green" />
              <h3 className="text-xl font-black">{card.label}</h3>
              <p className="mt-2 text-sm text-slate-500">{card.copy}</p>
            </button>
          );
        })}
      </section>

      <section className="mt-6 grid gap-6 lg:grid-cols-3">
        <div className="panel lg:col-span-2">
          <h2 className="text-2xl font-black">System Overview</h2>
          <p className="mt-2 text-slate-600">This project is now a multi-page React app backed by Flask APIs for disease detection, crop recommendation, fertilizer suggestion, weather, and authentication.</p>
          <div className="mt-5 grid gap-3 md:grid-cols-3">
            <div className="metric">Frontend <strong>React + Tailwind</strong></div>
            <div className="metric">Backend <strong>Flask API</strong></div>
            <div className="metric">AI <strong>PyTorch/OpenCV</strong></div>
          </div>
        </div>
        <div className="panel">
          <h2 className="text-2xl font-black">API Health</h2>
          <HealthCheck />
        </div>
      </section>
    </>
  );
}

function DiseasePage() {
  const { t } = useApp();
  const [diseaseResult, setDiseaseResult] = useState(null);
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function predictDisease(event) {
    event.preventDefault();
    setError("");
    const image = event.currentTarget.image.files[0];
    if (!image) {
      setError("Please choose a plant leaf image.");
      return;
    }
    const data = new FormData();
    data.append("image", image);
    setLoading(true);
    try {
      const response = await api.post("/predict-disease", data, { headers: { "Content-Type": "multipart/form-data" } });
      setDiseaseResult(response.data);
    } catch (requestError) {
      setError(requestError.response?.data?.error || "Disease prediction failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageShell eyebrow="POST /api/predict-disease" title={t.detect} subtitle="Upload a plant leaf image. The backend uses a trained CNN when available and OpenCV fallback otherwise.">
      <div className="grid gap-6 lg:grid-cols-[.9fr_1.1fr]">
        <form className="panel" onSubmit={predictDisease}>
          <h2 className="mb-1 text-2xl font-black">{t.upload}</h2>
          <p className="mb-4 text-sm text-slate-500">The image is sent to Flask, stored, processed, and saved in prediction history.</p>
          <label className="grid min-h-80 cursor-pointer place-items-center rounded-lg border-2 border-dashed border-agro-green/30 bg-agro-mint p-5 text-center">
            <input
              className="hidden"
              name="image"
              type="file"
              accept="image/*"
              onChange={(event) => {
                const file = event.target.files?.[0];
                setPreview(file ? URL.createObjectURL(file) : "");
              }}
            />
            {preview ? <img src={preview} className="max-h-72 rounded-lg object-cover" alt="leaf preview" /> : <Upload className="h-12 w-12 text-agro-green" />}
            <span className="mt-3 font-bold text-agro-green">Choose leaf image</span>
          </label>
          {error && <p className="mt-3 rounded-lg bg-red-50 p-3 text-sm font-semibold text-red-700">{error}</p>}
          <button className="btn-primary mt-4 w-full" disabled={loading}>{loading ? "Analyzing..." : t.analyze}</button>
        </form>

        <ResultPanel title="Disease Result" result={diseaseResult}>
          {diseaseResult && <DiseaseResult result={diseaseResult} />}
        </ResultPanel>
      </div>
    </PageShell>
  );
}

function CropPage() {
  const { t } = useApp();
  const [cropResult, setCropResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function recommendCrop(event) {
    event.preventDefault();
    setLoading(true);
    try {
      const payload = Object.fromEntries(new FormData(event.currentTarget).entries());
      const response = await api.post("/recommend-crop", payload);
      setCropResult(response.data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageShell eyebrow="POST /api/recommend-crop" title={t.crop} subtitle="Enter soil and climate values to receive a machine-learning crop recommendation.">
      <div className="grid gap-6 lg:grid-cols-[1fr_.8fr]">
        <form className="panel" onSubmit={recommendCrop}>
          <h2 className="mb-4 text-2xl font-black">Soil & Climate Inputs</h2>
          <InputGrid fields={["nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph", "rainfall"]} defaults={[40, 30, 30, 31, 68, 6.5, 200]} />
          <input name="location" className="input mt-3" defaultValue="Raipur" placeholder="Location" />
          <button className="btn-primary mt-4" disabled={loading}>{loading ? "Recommending..." : "Recommend crop"}</button>
        </form>
        <ResultPanel title="Recommendation" result={cropResult}>
          {cropResult && <Output title={cropResult.crop} subtitle={`Confidence ${(cropResult.confidence * 100).toFixed(1)}% · ${cropResult.model_version}`} />}
        </ResultPanel>
      </div>
    </PageShell>
  );
}

function FertilizerPage() {
  const { t } = useApp();
  const [fertilizerResult, setFertilizerResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function suggestFertilizer(event) {
    event.preventDefault();
    setLoading(true);
    try {
      const payload = Object.fromEntries(new FormData(event.currentTarget).entries());
      const response = await api.post("/suggest-fertilizer", payload);
      setFertilizerResult(response.data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageShell eyebrow="POST /api/suggest-fertilizer" title={t.fertilizer} subtitle="Compare soil nutrients with crop targets and get fertilizer guidance.">
      <div className="grid gap-6 lg:grid-cols-[1fr_.8fr]">
        <form className="panel" onSubmit={suggestFertilizer}>
          <h2 className="mb-4 text-2xl font-black">Nutrient Values</h2>
          <InputGrid fields={["nitrogen", "phosphorus", "potassium"]} defaults={[30, 20, 20]} />
          <input name="crop" className="input mt-3" defaultValue="rice" placeholder="Crop type" />
          <button className="btn-primary mt-4" disabled={loading}>{loading ? "Analyzing..." : "Suggest fertilizer"}</button>
        </form>
        <ResultPanel title="Fertilizer Plan" result={fertilizerResult}>
          {fertilizerResult && <FertilizerResult result={fertilizerResult} />}
        </ResultPanel>
      </div>
    </PageShell>
  );
}

function WeatherPage() {
  const { t } = useApp();
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);

  async function loadWeather() {
    setLoading(true);
    try {
      const response = await api.get("/weather?lat=21.2514&lon=81.6296");
      setWeather(response.data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadWeather();
  }, []);

  return (
    <PageShell eyebrow="GET /api/weather" title={t.weather} subtitle="Fetch real-time climate data for crop and disease-risk decisions.">
      <section className="panel">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-2xl font-black">Raipur, Chhattisgarh</h2>
            <p className="text-sm text-slate-500">Open-Meteo integration with fallback data when network is unavailable.</p>
          </div>
          <button className="btn-secondary" onClick={loadWeather}>{loading ? "Fetching..." : "Refresh weather"}</button>
        </div>
        {weather ? (
          <div className="mt-5 grid gap-3 md:grid-cols-4">
            <div className="metric">Temperature <strong>{weather.temperature}°C</strong></div>
            <div className="metric">Humidity <strong>{weather.humidity}%</strong></div>
            <div className="metric">Rainfall <strong>{weather.rainfall} mm</strong></div>
            <div className="metric">Wind <strong>{weather.wind_speed} km/h</strong></div>
          </div>
        ) : (
          <p className="mt-4 text-slate-500">Loading weather...</p>
        )}
      </section>
    </PageShell>
  );
}

function LoginPage() {
  const [mode, setMode] = useState("login");
  const [message, setMessage] = useState("");

  async function submitAuth(event) {
    event.preventDefault();
    setMessage("");
    const payload = Object.fromEntries(new FormData(event.currentTarget).entries());
    const endpoint = mode === "login" ? "/auth/login" : "/auth/register";
    try {
      const response = await api.post(endpoint, payload);
      localStorage.setItem("smart_agro_token", response.data.token);
      setMessage(`Signed in as ${response.data.user.name}`);
    } catch (error) {
      setMessage(error.response?.data?.error || "Authentication failed.");
    }
  }

  return (
    <PageShell eyebrow="Optional JWT auth" title="Account Access" subtitle="Basic authentication for future protected dashboards and prediction history.">
      <form className="panel mx-auto max-w-xl" onSubmit={submitAuth}>
        <div className="mb-4 flex gap-2">
          <button type="button" className={mode === "login" ? "btn-primary" : "btn-secondary"} onClick={() => setMode("login")}>Login</button>
          <button type="button" className={mode === "register" ? "btn-primary" : "btn-secondary"} onClick={() => setMode("register")}>Register</button>
        </div>
        {mode === "register" && <input className="input mb-3" name="name" placeholder="Name" defaultValue="Farmer" />}
        <input className="input mb-3" name="email" type="email" placeholder="Email" defaultValue="farmer@example.com" />
        <input className="input mb-4" name="password" type="password" placeholder="Password" defaultValue="password123" />
        <button className="btn-primary w-full">{mode === "login" ? "Login" : "Create account"}</button>
        {message && <p className="mt-3 rounded-lg bg-agro-mint p-3 text-sm font-semibold text-agro-green">{message}</p>}
      </form>
    </PageShell>
  );
}

function NotFoundPage() {
  const { navigate } = useApp();
  return (
    <PageShell eyebrow="404" title="Page not found" subtitle="The requested page does not exist in this React app.">
      <button className="btn-primary" onClick={() => navigate("/")}>Back to dashboard</button>
    </PageShell>
  );
}

function PageShell({ eyebrow, title, subtitle, children }) {
  return (
    <>
      <section className="mb-6">
        <p className="mb-3 inline-flex rounded-full bg-agro-mint px-3 py-1 text-xs font-bold text-agro-green">{eyebrow}</p>
        <h2 className="max-w-4xl text-4xl font-black leading-tight md:text-5xl">{title}</h2>
        <p className="mt-3 max-w-3xl text-slate-600">{subtitle}</p>
      </section>
      {children}
    </>
  );
}

function HealthCheck() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    api.get("/health")
      .then((response) => setStatus(`${response.data.status} · ${response.data.service}`))
      .catch(() => setStatus("Backend not reachable"));
  }, []);

  return <p className="mt-2 rounded-lg bg-agro-mint p-3 text-sm font-semibold text-agro-green">{status}</p>;
}

function ResultPanel({ title, result, children }) {
  return (
    <section className="panel">
      <h2 className="mb-1 text-2xl font-black">{title}</h2>
      {!result ? <p className="text-slate-500">No result yet. Submit the form to call the backend API.</p> : children}
    </section>
  );
}

function DiseaseResult({ result }) {
  return (
    <>
      <h3 className="text-3xl font-black">{result.disease_name}</h3>
      <p className="mt-2 text-slate-600">Confidence: {(result.confidence * 100).toFixed(1)}%</p>
      <div className="my-4 h-2 overflow-hidden rounded-full bg-black/10">
        <div className="h-full rounded-full bg-agro-green" style={{ width: `${result.confidence * 100}%` }} />
      </div>
      {result.metrics && (
        <div className="mb-4 grid gap-2 sm:grid-cols-2">
          {Object.entries(result.metrics).map(([key, value]) => (
            <div className="metric" key={key}>{key.replaceAll("_", " ")}: <strong>{value}</strong></div>
          ))}
        </div>
      )}
      <ul className="list-inside list-disc space-y-1 text-slate-700">
        {result.treatment.map((item) => <li key={item}>{item}</li>)}
      </ul>
    </>
  );
}

function FertilizerResult({ result }) {
  return (
    <div className="rounded-lg bg-agro-mint p-4">
      <h3 className="text-2xl font-black text-agro-green">{result.status}</h3>
      <p className="mt-2 text-slate-700">{result.recommendation}</p>
      {result.details && (
        <div className="mt-4 grid gap-2 sm:grid-cols-3">
          {Object.entries(result.details).map(([key, value]) => (
            <div className="metric" key={key}>{key}: <strong>{Number(value).toFixed(1)}</strong></div>
          ))}
        </div>
      )}
    </div>
  );
}

function InputGrid({ fields, defaults }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {fields.map((field, index) => (
        <label className="text-sm font-bold capitalize text-slate-600" key={field}>
          {field}
          <input className="input mt-1" name={field} type="number" step="0.1" defaultValue={defaults[index]} />
        </label>
      ))}
    </div>
  );
}

function Output({ title, subtitle }) {
  return (
    <div className="rounded-lg bg-agro-mint p-4">
      <h3 className="text-2xl font-black capitalize text-agro-green">{title}</h3>
      <p className="mt-1 text-sm text-slate-600">{subtitle}</p>
    </div>
  );
}

function useApp() {
  return useContext(AppContext);
}

createRoot(document.getElementById("root")).render(<App />);
