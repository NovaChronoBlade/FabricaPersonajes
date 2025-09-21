
"use client";

import CharacterMenu from "../components/CharacterMenu";

export default function Home() {
  // Reemplaza la URL por la de tu API real si la tienes
  const apiUrl = "http://127.0.0.1:5000/api/factories";

  function handleSelect(characterId: string) {
    // Aquí puedes manejar la selección del personaje
    console.log("Personaje seleccionado:", characterId);
  }

  return (
    <main >
      <CharacterMenu apiUrl={apiUrl} onSelect={handleSelect} />
    </main>
  );
}
