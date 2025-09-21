import React, { useState, useEffect } from "react";
import { DeleteResponse } from "../types/character";

interface DeleteButtonProps {
  selectedRace: string;
  onDelete?: () => void;
  disabled?: boolean;
}

const DeleteButton: React.FC<DeleteButtonProps> = ({
  selectedRace,
  onDelete,
  disabled = false,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Auto-limpiar mensajes de error después de 5 segundos
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  // Auto-limpiar mensajes de éxito después de 5 segundos
  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => {
        setSuccess(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [success]);

  const handleDelete = async () => {
    if (!selectedRace) {
      alert("🚫 Debes seleccionar una raza antes de eliminar.");
      return;
    }

    // Confirmar la eliminación
    const confirmDelete = window.confirm(
      `¿Estás seguro de que quieres eliminar la fábrica de héroes ${selectedRace}? Esta acción no se puede deshacer.`
    );

    if (!confirmDelete) {
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/pool/delete/${selectedRace}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data: DeleteResponse = await response.json();

      if (response.ok && data.success === true) {
        setSuccess(data.message || "Fábrica eliminada exitosamente");
        if (onDelete) {
          onDelete();
        }
      } else {
        throw new Error(data.message || "Error al eliminar la fábrica");
      }
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Error al eliminar la fábrica"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <button
        onClick={handleDelete}
        disabled={!selectedRace || loading || disabled}
        className="w-full bg-gradient-to-r from-red-600 to-red-800 hover:from-red-700 hover:to-red-900 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-lg disabled:hover:scale-100 shadow-lg"
      >
        {loading ? (
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            🗑️ Eliminando fábrica...
          </div>
        ) : (
          "🗑️ Eliminar Fábrica"
        )}
      </button>

      {error && (
        <div className="p-4 bg-red-500/20 rounded-xl border border-red-400/30 text-red-300 text-center">
          ❌ {error}
        </div>
      )}

      {success && (
        <div className="p-4 bg-green-500/20 rounded-xl border border-green-400/30 text-green-300 text-center">
          ✅ {success}
        </div>
      )}
    </div>
  );
};

export default DeleteButton;