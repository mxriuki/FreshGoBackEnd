from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

# Recipe model
class Recipe(BaseModel):
    id: UUID
    title: str
    ingredients: List[str]
    instructions: str
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None

# In-memory "database"
recipes_db: List[Recipe] = [
    Recipe(
        id=uuid4(),
        title="Recipe 1", 
        ingredients=["Ingredient 1", "Ingredient 2"],
        instructions="Instructions 1",
        tags=["Tag 1", "Tag 2"],
        image_url="https://example.com/image1.jpg"
    ),
    Recipe(
        id=uuid4(),
        title="Recipe 2",
        ingredients=["Ingredient 3", "Ingredient 4"],
        instructions="Instructions 2",
        tags=["Tag 3", "Tag 4"],
        image_url="https://example.com/image2.jpg"
    ),
    Recipe(
        id=uuid4(),
        title="Recipe 3",
        ingredients=["Ingredient 5", "Ingredient 6"],
        instructions="Instructions 3",
        tags=["Tag 5", "Tag 6"],
        image_url="https://example.com/image3.jpg"
    ),
    Recipe(
        id=uuid4(),
        title="Recipe 4",
        ingredients=["Ingredient 7", "Ingredient 8"],
        instructions="Instructions 4",
        tags=["Tag 7", "Tag 8"],
        image_url="https://example.com/image4.jpg"
    ),
]

# Create a new recipe
@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe):
    if any(r.id == recipe.id for r in recipes_db):
        raise HTTPException(status_code=400, detail="Recipe ID already exists")
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
