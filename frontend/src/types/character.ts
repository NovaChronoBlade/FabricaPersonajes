// Tipos para la respuesta de la API
export interface CharacterBody {
  cuerpo_img: string | null;
  especie: string;
  altura: string;
  peso: string;
  habilidades: string[];
}

export interface CharacterMount {
  imagen: string | null;
  tipo: string;
  velocidad: string;
  habilidades: string[];
}

export interface CharacterArmor {
  imagen: string | null;
  tipo: string;
  material: string;
  defensa: string;
  peso: string;
}

export interface CharacterWeapon {
  imagen: string | null;
  tipo: string;
  material: string;
  daño: string;
  alcance: string;
}

export interface Character {
  cuerpo: CharacterBody;
  montura: CharacterMount;
  armadura: CharacterArmor;
  arma: CharacterWeapon;
}

export interface ApiResponse {
  status: string;
  kind: string;
  character: Character;
  message?: string;
  error?: string;
}

export interface DeleteResponse {
  status: string;
  message: string;
  error?: string;
  success?: boolean;
}