import type { CoffeeBean } from "./bean";
import type { User } from "./user";

export interface BrewStep {
  step_number: number;
  description: string;
  duration_seconds: number;
}

export interface BrewRecipe {
  id: number;
  user_id: number;
  bean_id: number | null;
  name: string;
  device: string;
  water_temp: number;
  grind_size: string;
  ratio: string;
  steps: BrewStep[];
  created_at: string;
  user: User | null;
  bean: CoffeeBean | null;
}

export interface RecipePayload {
  name: string;
  device: string;
  water_temp: number;
  grind_size: string;
  ratio: string;
  steps: BrewStep[];
  bean_id: number | null;
}

