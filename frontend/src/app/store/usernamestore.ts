import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface AppState {
  username: string;
  setUsername: (newusername: string) => void;
}

const useStore = create<AppState>()(
  persist<AppState>(
    (set) => ({
      // Initial State
      username: "Aziz",

      // Basic Setters
      setUsername: (newusername: string) => set({ username: newusername }),
    }),
    {
      name: "app-storage",
    },
  ),
);

export default useStore;
