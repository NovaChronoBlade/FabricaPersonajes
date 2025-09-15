"use client";

import Image from "next/image";
import { useEffect, useState } from "react";

type Character = Record<string, any>;

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:5000";

export default function Home() {
  const [factories, setFactories] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [info, setInfo] = useState<Record<string, any> | null>(null);
  const [created, setCreated] = useState<Record<string, any> | null>(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/factories`)
      .then((r) => r.json())
      .then((data) => setFactories(Array.isArray(data) ? data : []))
      .catch((e) => setError(String(e)));
  }, []);

  async function handleInfo(kind: string) {
    setLoading(true);
    setError(null);
    setInfo(null);
    try {
      const res = await fetch(`${BACKEND_URL}/api/character/${kind}/info`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setInfo(data);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(kind: string) {
    setLoading(true);
    setError(null);
    setCreated(null);
    try {
      const res = await fetch(`${BACKEND_URL}/api/create/${kind}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setCreated(data);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[24px] row-start-2 items-center sm:items-start w-full max-w-3xl">
        <header className="flex items-center gap-4">
          <Image className="dark:invert" src="/next.svg" alt="Next.js" width={120} height={28} />
          <h1 className="text-2xl font-semibold">Consumo de backend</h1>
        </header>

        <section className="w-full bg-white/60 dark:bg-black/40 rounded-lg p-4">

          <div className="mb-4">
            <h2 className="font-medium">Fábricas</h2>
            {factories.length === 0 ? (
              <div className="text-gray-600">No hay fábricas disponibles.</div>
            ) : (
              <div className="flex gap-2 flex-wrap mt-2">
                {factories.map((f) => (
                  <div key={f} className="flex items-center gap-2">
                    <button className="px-3 py-1 rounded bg-slate-800 text-white" onClick={() => { setSelected(f); handleInfo(f); }}>
                      Info
                    </button>
                    <button className="px-3 py-1 rounded border" onClick={() => handleCreate(f)}>
                      Crear {f}
                    </button>
                    <div className="ml-2 text-sm">{f}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mt-4">
            {loading && <div>Cargando...</div>}
            {error && <div className="text-red-600">Error: {error}</div>}

            {info && (
              <div className="mt-3 p-3 border rounded">
                <h3 className="font-semibold">Info: {selected}</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                  {['cuerpo', 'montura', 'armadura', 'arma'].map((key) => {
                    const section = (info as any)[key];
                    if (!section) return null;
                    return (
                      <div key={key} className="p-3 border rounded">
                        <h4 className="font-semibold capitalize">{key}</h4>
                        {section.cuerpo_img || section.imagen ? (
                          // Preferir rutas relativas que vengan desde backend
                          <img
                            src={
                              String(section.cuerpo_img || section.imagen).startsWith("/")
                                ? `${BACKEND_URL}${String(section.cuerpo_img || section.imagen)}`
                                : String(section.cuerpo_img || section.imagen)
                            }
                            alt={`${key} image`}
                            className="w-full h-36 object-contain my-2 bg-white"
                          />
                        ) : null}
                        <ul className="text-sm space-y-1">
                          {Object.entries(section).map(([k, v]) => {
                            if (k === 'cuerpo_img' || k === 'imagen') return null;
                            if (Array.isArray(v)) {
                              return (
                                <li key={k}>
                                  <strong>{k}:</strong>
                                  <ul className="pl-4 list-disc">
                                    {v.map((it: any, i: number) => (
                                      <li key={i} className="text-sm">{String(it)}</li>
                                    ))}
                                  </ul>
                                </li>
                              );
                            }
                            return (
                              <li key={k}>
                                <strong>{k}:</strong> <span className="ml-1">{String(v)}</span>
                              </li>
                            );
                          })}
                        </ul>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {created && (
              <div className="mt-3 p-3 border rounded bg-green-700">
                <h3 className="font-semibold">Creado</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                  {['cuerpo', 'montura', 'armadura', 'arma'].map((key) => {
                    const section = (created as any).character?.[key];
                    if (!section) return null;
                    return (
                      <div key={key} className="p-3 border rounded">
                        <h4 className="font-semibold capitalize">{key}</h4>
                        {section.cuerpo_img || section.imagen ? (
                          <img
                            src={
                              String(section.cuerpo_img || section.imagen).startsWith("/")
                                ? `${BACKEND_URL}${String(section.cuerpo_img || section.imagen)}`
                                : String(section.cuerpo_img || section.imagen)
                            }
                            alt={`${key} image`}
                            className="w-full h-36 object-contain my-2 bg-white"
                          />
                        ) : null}
                        <ul className="text-sm space-y-1">
                          {Object.entries(section).map(([k, v]) => {
                            if (k === 'cuerpo_img' || k === 'imagen') return null;
                            if (Array.isArray(v)) {
                              return (
                                <li key={k}>
                                  <strong>{k}:</strong>
                                  <ul className="pl-4 list-disc">
                                    {v.map((it: any, i: number) => (
                                      <li key={i} className="text-sm">{String(it)}</li>
                                    ))}
                                  </ul>
                                </li>
                              );
                            }
                            return (
                              <li key={k}>
                                <strong>{k}:</strong> <span className="ml-1">{String(v)}</span>
                              </li>
                            );
                          })}
                        </ul>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </section>

      </main>
    </div>
  );
}
