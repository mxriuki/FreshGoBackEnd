from fastapi import FastAPI, HTTPException  # type: ignore
from pydantic import BaseModel  # type: ignore
from fastapi.middleware.cors import CORSMiddleware 
from typing import List, Optional
from uuid import UUID, uuid4
import uvicorn  # type: ignore
import requests  # type: ignore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

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

# Adding initial recipes to the in-memory database
initial_recipes = [
    {
        "title": "Spaghetti Carbonara",
        "ingredients": [
            "200g spaghetti",
            "100g pancetta",
            "2 large eggs",
            "50g grated Pecorino cheese",
            "50g grated Parmesan cheese",
            "Black pepper",
            "Salt"
        ],
        "instructions": "Cook the spaghetti in salted boiling water until al dente. In a separate pan, cook the pancetta until crispy. Beat the eggs and mix with the cheeses. Drain the spaghetti and mix everything together quickly while the pasta is still hot. Serve immediately with extra cheese and black pepper.",
        "tags": ["Italian", "Pasta", "Main Course"],
        "image_url": "https://i.pinimg.com/564x/37/98/2a/37982ab7e39b965ddad554764f68531e.jpg"
    },
    {
        "title": "Chicken Tikka Masala",
        "ingredients": [
            "500g chicken breast, diced",
            "200g yogurt",
            "2 tbsp tikka masala paste",
            "1 onion, chopped",
            "400g canned tomatoes",
            "100ml cream",
            "Fresh coriander",
            "Salt"
        ],
        "instructions": "Marinate chicken in yogurt and tikka paste for at least an hour. Cook onion until soft, then add marinated chicken. Cook until chicken is browned, add tomatoes and simmer. Stir in cream and garnish with coriander.",
        "tags": ["Indian", "Curry", "Main Course"],
        "image_url": "https://i.pinimg.com/564x/c6/65/c7/c665c758a0b5d5a6a93db951d11124d1.jpg"
    },
    {
        "title": "Beef Tacos",
        "ingredients": [
            "400g minced beef",
            "1 onion, diced",
            "2 cloves garlic, minced",
            "1 tsp chili powder",
            "1 tsp cumin",
            "Taco shells",
            "Lettuce, tomato, cheese, sour cream"
        ],
        "instructions": "Brown the minced beef with onion and garlic. Add spices and cook for a few minutes. Serve in taco shells with your choice of toppings.",
        "tags": ["Mexican", "Fast Food", "Main Course"],
        "image_url": "https://i.pinimg.com/564x/78/0d/1d/780d1d277113b6fc7db6ff6b0c99b402.jpg"
    },
    {
        "title": "Vegetable Stir Fry",
        "ingredients": [
            "1 cup broccoli florets",
            "1 bell pepper, sliced",
            "1 carrot, julienned",
            "2 cloves garlic, minced",
            "2 tbsp soy sauce",
            "1 tbsp sesame oil",
            "Cooked rice"
        ],
        "instructions": "Heat sesame oil in a pan, add garlic and vegetables. Stir-fry until tender. Add soy sauce and serve over cooked rice.",
        "tags": ["Vegetarian", "Quick Meal", "Main Course"],
        "image_url": "https://i.pinimg.com/564x/9a/f6/50/9af650df61443471f0170cc7a15e81af.jpg"
    },
    {
        "title": "Chocolate Chip Cookies",
        "ingredients": [
            "125g butter",
            "100g brown sugar",
            "1 egg",
            "200g flour",
            "1 tsp baking soda",
            "100g chocolate chips"
        ],
        "instructions": "Cream butter and sugar, add egg. Mix flour and baking soda, then combine with wet ingredients. Fold in chocolate chips. Bake at 180°C for 10-12 minutes.",
        "tags": ["Dessert", "Baking", "Snack"],
        "image_url": "https://i.pinimg.com/564x/79/38/7b/79387b805465a32632ec124beee05e8e.jpg"
    }
]

# Populate the in-memory database with initial recipes
for recipe_data in initial_recipes:
    recipe = Recipe(**recipe_data)
    recipe.id = uuid4()  # Assign a new UUID to each recipe
    recipes_db.append(recipe)

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