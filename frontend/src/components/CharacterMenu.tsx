import React, { useState, useEffect } from "react";
import { Character, ApiResponse } from "../types/character";
import { getImageUrl } from "../lib/getImageUrl";
import RaceSelector from "./RaceSelector";
import CharacterCard, { InfoItem, AbilitiesList } from "./CharacterCard";
import DeleteButton from "./DeleteButton";

interface CharacterMenuProps {
  apiUrl: string;
  onSelect: (raza: string) => void;
}

const CharacterMenu: React.FC<CharacterMenuProps> = ({ apiUrl, onSelect }) => {
  const [character, setCharacter] = useState<Character | null>(null);
  const [loadingCharacter, setLoadingCharacter] = useState(false);
  const [characterError, setCharacterError] = useState<string | null>(null);
  const [selectedRace, setSelectedRace] = useState<string>("");

  // Auto-limpiar mensajes de error después de 5 segundos
  useEffect(() => {
    if (characterError) {
      const timer = setTimeout(() => {
        setCharacterError(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [characterError]);

  const handleRaceChange = (race: string) => {
    setSelectedRace(race);
    onSelect(race);
  };

  const handleDelete = () => {
    // Limpiar el personaje actual después de eliminar
    setCharacter(null);
    setCharacterError(null);
  };

  const createCharacter = async () => {
    if (!selectedRace) {
      alert("🎭 Debes seleccionar una raza antes de crear tu héroe.");
      return;
    }

    setLoadingCharacter(true);
    setCharacterError(null);
    setCharacter(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/create/${selectedRace}`
      );
      const data: ApiResponse = await response.json();

      if (data.status === "created") {
        setCharacter(data.character);
      } else {
        if (data.error) {
          throw new Error(data.message || "Error al forjar tu héroe");
        }
        throw new Error("");
      }
    } catch (error) {
      setCharacterError(
        error instanceof Error ? error.message : "Error al forjar tu héroe"
      );
    } finally {
      setLoadingCharacter(false);
    }
  };

  return (
    <div
      className="min-h-screen p-6 relative overflow-hidden bg-cover bg-center"
      style={{
        backgroundImage: "url('/wallpaperbetter.jpg')",
        backgroundAttachment: "fixed",
      }}
    >
      {/* Capa de overlay para mejor legibilidad */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/70 via-blue-900/60 to-indigo-900/70"></div>

      {/* Efectos de fondo decorativos */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-yellow-500 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl animate-pulse animation-delay-4000"></div>
      </div>

      <div className="relative z-10 flex flex-col lg:flex-row gap-8 max-w-7xl mx-auto">
        {/* Panel de selección mejorado */}
        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl shadow-2xl p-8 lg:w-96 flex-shrink-0 transition-all duration-300 hover:bg-white/15">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text">
              ⚔️ Creador de Héroes
            </h2>
            <p className="text-gray-300">Forja tu leyenda</p>
          </div>

          <div className="space-y-6">
            <RaceSelector
              apiUrl={apiUrl}
              selectedRace={selectedRace}
              onRaceChange={handleRaceChange}
            />

            <button
              onClick={createCharacter}
              disabled={!selectedRace || loadingCharacter}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-lg disabled:hover:scale-100 shadow-lg"
            >
              {loadingCharacter ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  ⚡ Forjando héroe...
                </div>
              ) : (
                "🎲 Crear Héroe"
              )}
            </button>

            <DeleteButton
              selectedRace={selectedRace}
              onDelete={handleDelete}
              disabled={loadingCharacter}
            />

            {characterError && (
              <div className="p-4 bg-red-500/20 rounded-xl border border-red-400/30 text-red-300 text-center">
                ❌ {characterError}
              </div>
            )}
          </div>
        </div>

        {/* Panel de detalles del personaje mejorado */}
        <div className="flex-1">
          {character && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in">
              {/* CUERPO */}
              <CharacterCard
                title="Forma Física"
                icon="🧬"
                image={character.cuerpo.cuerpo_img}
                gradientFrom="from-blue-400"
                gradientTo="to-purple-500"
                colorClass="text-blue-300"
                fallbackEmoji="🧬"
              >
                <InfoItem
                  label="👤 Especie:"
                  value={character.cuerpo.especie}
                  colorClass="text-blue-300"
                />
                <InfoItem
                  label="📏 Altura:"
                  value={character.cuerpo.altura}
                  colorClass="text-blue-300"
                />
                <InfoItem
                  label="⚖️ Peso:"
                  value={character.cuerpo.peso}
                  colorClass="text-blue-300"
                />
                <AbilitiesList
                  abilities={character.cuerpo.habilidades}
                  colorClass="text-blue-300"
                  label="✨ Habilidades:"
                />
              </CharacterCard>

              {/* MONTURA */}
              <CharacterCard
                title="Compañero"
                icon="🐎"
                image={character.montura.imagen}
                gradientFrom="from-green-400"
                gradientTo="to-blue-500"
                colorClass="text-green-300"
                fallbackEmoji="🐎"
              >
                <InfoItem
                  label="🦄 Tipo:"
                  value={character.montura.tipo}
                  colorClass="text-green-300"
                />
                <InfoItem
                  label="💨 Velocidad:"
                  value={character.montura.velocidad}
                  colorClass="text-green-300"
                />
                <AbilitiesList
                  abilities={character.montura.habilidades}
                  colorClass="text-green-300"
                  label="🌟 Habilidades:"
                />
              </CharacterCard>

              {/* ARMADURA */}
              <CharacterCard
                title="Protección"
                icon="🛡️"
                image={character.armadura.imagen}
                gradientFrom="from-yellow-400"
                gradientTo="to-red-500"
                colorClass="text-yellow-300"
                fallbackEmoji="🛡️"
              >
                <InfoItem
                  label="⚔️ Tipo:"
                  value={character.armadura.tipo}
                  colorClass="text-yellow-300"
                />
                <InfoItem
                  label="🔨 Material:"
                  value={character.armadura.material}
                  colorClass="text-yellow-300"
                />
                <InfoItem
                  label="🛡️ Defensa:"
                  value={character.armadura.defensa}
                  colorClass="text-yellow-300"
                />
                <InfoItem
                  label="⚖️ Peso:"
                  value={character.armadura.peso}
                  colorClass="text-yellow-300"
                />
              </CharacterCard>

              {/* ARMA */}
              <CharacterCard
                title="Arsenal"
                icon="⚔️"
                image={character.arma.imagen}
                gradientFrom="from-red-400"
                gradientTo="to-purple-500"
                colorClass="text-red-300"
                fallbackEmoji="⚔️"
              >
                <InfoItem
                  label="🗡️ Tipo:"
                  value={character.arma.tipo}
                  colorClass="text-red-300"
                />
                <InfoItem
                  label="🔨 Material:"
                  value={character.arma.material}
                  colorClass="text-red-300"
                />
                <InfoItem
                  label="💥 Daño:"
                  value={character.arma.daño}
                  colorClass="text-red-300"
                />
                <InfoItem
                  label="📏 Alcance:"
                  value={character.arma.alcance}
                  colorClass="text-red-300"
                />
              </CharacterCard>
            </div>
          )}

          {/* Mensaje inicial cuando no hay personaje */}
          {!character && !loadingCharacter && (
            <div className="flex items-center justify-center h-96">
              <div className="text-center text-white/70">
                <div className="text-6xl mb-4">🏰</div>
                <h3 className="text-2xl font-bold mb-2">
                  ¡Aventura te espera!
                </h3>
                <p className="text-lg">
                  Selecciona una raza y crea tu héroe legendario
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.6s ease-out;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
};

export default CharacterMenu;
