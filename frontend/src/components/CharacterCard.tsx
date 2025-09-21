import React from "react";
import { getImageUrl } from "../lib/getImageUrl";

interface CharacterCardProps {
  title: string;
  icon: string;
  image: string | null;
  gradientFrom: string;
  gradientTo: string;
  colorClass: string;
  children: React.ReactNode;
  fallbackEmoji: string;
}

const CharacterCard: React.FC<CharacterCardProps> = ({
  title,
  icon,
  image,
  gradientFrom,
  gradientTo,
  colorClass,
  children,
  fallbackEmoji,
}) => {
  return (
    <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl shadow-2xl p-6 transition-all duration-300 hover:bg-white/15 hover:scale-105 group">
      <div className="flex flex-col items-center text-center">
        <div className={`w-36 h-36 rounded-full bg-gradient-to-r ${gradientFrom} ${gradientTo} p-1 mb-4 group-hover:scale-110 transition-transform duration-300 flex items-center justify-center`}>
          {getImageUrl(image) ? (
            <img
              src={getImageUrl(image)!}
              alt={title}
              className="w-full h-full rounded-full object-cover"
            />
          ) : (
            <div className="text-4xl">{fallbackEmoji}</div>
          )}
        </div>
        <h3 className="text-2xl font-bold mb-4 text-white flex items-center">
          {icon}{" "}
          <span className={`ml-2 bg-gradient-to-r ${gradientFrom} ${gradientTo} bg-clip-text text-transparent`}>
            {title}
          </span>
        </h3>
        <div className="space-y-3 text-left w-full">
          {children}
        </div>
      </div>
    </div>
  );
};

// Componente específico para mostrar habilidades
interface AbilitiesListProps {
  abilities: string[];
  colorClass: string;
  label: string;
}

export const AbilitiesList: React.FC<AbilitiesListProps> = ({
  abilities,
  colorClass,
  label,
}) => (
  <div className="mt-4">
    <span className={`font-semibold ${colorClass}`}>
      {label}
    </span>
    <ul className="list-none mt-2 space-y-1">
      {abilities.map((ability: string, i: number) => (
        <li key={i} className="text-gray-300 pl-4 relative">
          <span className="absolute left-0">•</span>
          {ability}
        </li>
      ))}
    </ul>
  </div>
);

// Componente para mostrar información básica
interface InfoItemProps {
  label: string;
  value: string;
  colorClass: string;
}

export const InfoItem: React.FC<InfoItemProps> = ({
  label,
  value,
  colorClass,
}) => (
  <p className="text-gray-300">
    <span className={`font-semibold ${colorClass}`}>
      {label}
    </span>{" "}
    {value}
  </p>
);

export default CharacterCard;