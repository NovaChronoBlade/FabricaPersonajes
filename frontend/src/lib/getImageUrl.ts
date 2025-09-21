export function getImageUrl(path: string | null | undefined) {
  if (!path) return null;
  if (path.startsWith("http")) return path;
  const base = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:5000";
  // Asegurar que la ruta relativa no tenga doble slash
  return `${base.replace(/\/+$/,'')}${path.startsWith('/') ? path : `/${path}`}`;
}
