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
    allow_origins=["http://localhost:3000","https://freshgo-app.vercel.app/"],
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
        "image_url": "https://www.thespruceeats.com/thmb/ovIQQQxQajADuIE2lqhgqq7ppyE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/pasta-carbonara-recipe-5210168-hero-01-80090e56abc04ca19d88ebf7fad1d157.jpg"
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
        "image_url": "https://www.allrecipes.com/thmb/1ul-jdOz8H4b6BDrRcYOuNmJgt4=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/239867chef-johns-chicken-tikka-masala-ddmfs-3X4-0572-e02a25f8c7b745459a9106e9eb13de10.jpg"
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
        "image_url": "https://www.onceuponachef.com/images/2023/08/Beef-Tacos.jpg"
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
        "image_url": "https://therecipecritic.com/wp-content/uploads/2019/09/Vegetable-Stir-Fry-Facebook-SEO-800-x-534.png"
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
        "image_url": "https://assets.bonappetit.com/photos/5ca53449cab3b6de9ee488f4/16:9/w_2560%2Cc_limit/chocolate-chip-cookie-1.jpg"
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