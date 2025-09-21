import React, { useEffect, useState } from "react";

interface RaceSelectorProps {
  apiUrl: string;
  selectedRace: string;
  onRaceChange: (race: string) => void;
}

const RaceSelector: React.FC<RaceSelectorProps> = ({
  apiUrl,
  selectedRace,
  onRaceChange,
}) => {
  const [races, setRaces] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auto-limpiar mensajes de error después de 5 segundos
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  useEffect(() => {
    const fetchRaces = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(apiUrl);
        const data: string[] = await response.json();
        setRaces(Array.isArray(data) ? data : []);
      } catch (error) {
        setError(
          error instanceof Error ? error.message : "Error desconocido"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchRaces();
  }, [apiUrl]);

  const handleRaceChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onRaceChange(e.target.value);
  };

  return (
    <div className="space-y-4">
      <div>
        <label
          htmlFor="character-select"
          className="block text-lg font-semibold mb-3 text-white"
        >
          🏰 Selecciona tu raza:
        </label>
        {loading ? (
          <div className="flex items-center justify-center p-4 bg-blue-500/20 rounded-xl border border-blue-400/30">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-400"></div>
            <span className="ml-3 text-blue-300">
              Cargando razas mágicas...
            </span>
          </div>
        ) : error ? (
          <div className="p-4 bg-red-500/20 rounded-xl border border-red-400/30 text-red-300">
            ⚠️ Error: {error}
          </div>
        ) : (
          <select
            id="character-select"
            value={selectedRace}
            onChange={handleRaceChange}
            className="w-full p-4 text-lg rounded-xl border-2 border-white/20 bg-white/10 backdrop-blur-sm text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 focus:bg-white/15 transition-all duration-300 hover:bg-white/15"
          >
            <option value="" className="text-gray-800">
              -- Elige tu destino --
            </option>
            {races.map((raza, index) => (
              <option key={index} value={raza} className="text-gray-800">
                {raza.charAt(0).toUpperCase() + raza.slice(1)}
              </option>
            ))}
          </select>
        )}
      </div>

      {selectedRace && (
        <div className="p-4 bg-green-500/20 rounded-xl border border-green-400/30 text-center transform animate-pulse">
          <span className="text-green-300 font-semibold">
            ✨ Raza elegida:{" "}
            {selectedRace.charAt(0).toUpperCase() + selectedRace.slice(1)}
          </span>
        </div>
      )}
    </div>
  );
};

export default RaceSelector;