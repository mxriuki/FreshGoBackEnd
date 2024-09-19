from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Optional
from uuid import UUID, uuid4
import uvicorn # type: ignore
import requests # type: ignore

app = FastAPI()

# Recipe model
class Recipe(BaseModel):
    id: Optional[UUID] = None
    title: str
    ingredients: List[str]
    instructions: str
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None

# In-memory "database"
recipes_db: List[Recipe] = []

# Create a new recipe
@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe):
    recipe.id = uuid4()  # Generate a new UUID for the recipe
    recipes_db.append(recipe)
    return recipe

# Read all recipes
@app.get("/recipes/", response_model=List[Recipe])
def read_recipes():
    return recipes_db

# Read a specific recipe by ID
@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: UUID):
    for recipe in recipes_db:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

# Update a recipe by ID
@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: UUID, updated_recipe: Recipe):
    for index, recipe in enumerate(recipes_db):
        if recipe.id == recipe_id:
            updated_recipe.id = recipe.id  # Ensure the ID remains unchanged
            recipes_db[index] = updated_recipe
            return updated_recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

# Delete a recipe by ID
@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: UUID):
    for index, recipe in enumerate(recipes_db):
        if recipe.id == recipe_id:
            del recipes_db[index]
            return {"detail": "Recipe deleted"}
    raise HTTPException(status_code=404, detail="Recipe not found")

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


    new_recipe = {
        "title": "Spaghetti Carbonara",
        "ingredients": ["200g spaghetti", "100g pancetta", "2 large eggs", "50g grated Pecorino cheese", "50g grated Parmesan cheese", "Black pepper", "Salt"],
        "instructions": "Cook the spaghetti in salted boiling water until al dente. In a separate pan, cook the pancetta until crispy. Beat the eggs and mix with the cheeses. Drain the spaghetti and mix everything together quickly while the pasta is still hot. Serve immediately with extra cheese and black pepper.",
        "tags": ["Italian", "Pasta", "Main Course"],
        "image_url": "https://example.com/spaghetti_carbonara.jpg"
    }

    response = requests.post("http://127.0.0.1:8000/recipes/", json=new_recipe)
    print("Created Recipe:", response.json())

    # 2. Read All Recipes
    response = requests.get("http://127.0.0.1:8000/recipes/")
    print("All Recipes:", response.json())

    # 3. Read a Recipe by ID (use an actual UUID from created recipes)
    recipe_id = "valid-uuid-here"  # Replace with a valid UUID
    response = requests.get(f"http://127.0.0.1:8000/recipes/{recipe_id}")
    print("Recipe:", response.json())

    # 4. Update a Recipe
    updated_recipe = {
        "title": "Updated Recipe Title",
        "ingredients": ["Updated Ingredient 1", "Updated Ingredient 2"],
        "instructions": "Updated instructions.",
        "tags": ["Updated Tag"],
        "image_url": "https://example.com/new_image.jpg"
    }

    recipe_id = "valid-uuid-here"  # Replace with a valid UUID
    response = requests.put(f"http://127.0.0.1:8000/recipes/{recipe_id}", json=updated_recipe)
    print("Updated Recipe:", response.json())

    # 5. Delete a Recipe
    recipe_id = "valid-uuid-here"  # Replace with a valid UUID
    response = requests.delete(f"http://127.0.0.1:8000/recipes/{recipe_id}")
    print("Delete Response:", response.json())

