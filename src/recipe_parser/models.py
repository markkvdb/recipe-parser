from datetime import timedelta, datetime 
from enum import Enum
from typing import Literal
from textwrap import dedent

from pydantic import BaseModel, Field, HttpUrl, PositiveInt, PositiveFloat

class MeasurementUnit(str, Enum):
    # Volume
    ML = "ml"
    L = "l"
    TSP = "tsp"
    TBSP = "tbsp"
    
    # Weight
    G = "g"
    KG = "kg"
    
    # Count
    PIECE = "piece"
    PINCH = "pinch"
    TO_TASTE = "to_taste"

class MealCategory(str, Enum):
   # Main Categories
    MAIN_COURSE = "main_course"
    APPETIZER = "appetizer"
    SIDE_DISH = "side_dish"
    DESSERT = "dessert"
    BREAKFAST = "breakfast"
    BRUNCH = "brunch"
    
    # Baked Goods
    BREAD = "bread"
    PASTRY = "pastry"
    CAKE = "cake"
    COOKIE = "cookie"
    PIE = "pie"
    
    # Smaller Dishes
    SNACK = "snack"
    FINGER_FOOD = "finger_food"
    DIP = "dip"
    SAUCE = "sauce"
    CONDIMENT = "condiment"
    
    # Drinks
    BEVERAGE = "beverage"
    COCKTAIL = "cocktail"
    SMOOTHIE = "smoothie"
    
    # Soup & Salad
    SOUP = "soup"
    STEW = "stew"
    SALAD = "salad"

    # Special Categories
    PRESERVE = "preserve"
    SANDWICH = "sandwich"
    PASTA = "pasta"
    PIZZA = "pizza"
    
    # Meal Prep
    MEAL_PREP = "meal_prep"
    BATCH_COOKING = "batch_cooking"
    
    # Other
    OTHER = "other"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class WebSource(BaseModel):
    type: Literal["web"] = "web"
    url: HttpUrl = Field(
        description="The complete URL of the recipe source, including http:// or https://"
    )

class BookSource(BaseModel):
    type: Literal["book"] = "book"
    title: str = Field(
        description="The full title of the book"
    )
    author: str = Field(
        description="The full name of the book's author"
    )
    page: PositiveInt = Field(
        description="The page number where the recipe can be found"
    )
    isbn: str | None = Field(
        None,
        description="The ISBN-10 or ISBN-13 number of the book"
    )

class MagazineSource(BaseModel):
    type: Literal["magazine"] = "magazine"
    title: str = Field(
        description="The name of the magazine"
    )
    issue: str = Field(
        description="The issue identifier, e.g., 'March 2024' or 'Issue 123'"
    )
    page: int = Field(
        description="The page number where the recipe can be found"
    )

Source = WebSource | BookSource | MagazineSource

class Ingredient(BaseModel):
    name: str = Field(
        description=dedent(
            """
            The name of the ingredient, e.g., 'all-purpose flour' or 'unsalted butter'. Make sure
            to not include the quantity or unit in the name.
            """
        )
    )
    quantity: PositiveFloat = Field(
        description="The amount of the ingredient needed"
    )
    unit: MeasurementUnit = Field(
        description="The unit of measurement for the ingredient quantity"
    )
    notes: str | None = Field(
        None,
        description="Additional notes about the ingredient, e.g., 'room temperature' or 'finely chopped'"
    )

class Step(BaseModel):
    order: int = Field(
        description="The sequence number of this step in the recipe"
    )
    instruction: str = Field(
        description="The detailed instruction for this step of the recipe"
    )
    time: timedelta | None = Field(
        None,
        description="The estimated time for cooking, baking or preparation time."
    )
    note: str  | None = Field(
        None,
        description="All information that is not listed in the instruction but mentioned in the source."
    )

class RecipeSource(BaseModel):
    source: Source | None = Field(
        None,
        discriminator="type",
        description="The original source of this recipe, whether from the web, a book, or a magazine"
    )

class Recipe(BaseModel):
    # Basic Information
    title: str = Field(
        description="The name of the recipe"
    )
    description: str = Field(
        description="A brief description of the dish, including what it is and any notable features"
    )
    author: str = Field(
        description="The person who created or contributed this recipe"
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="The date and time when this recipe was created, in ISO format"
    )
    
    # Recipe Details
    prep_time: timedelta = Field(
        description="The time needed for preparation before cooking"
    )
    cook_time: timedelta = Field(
        description="The time needed for cooking"
    )
    total_time: timedelta = Field(
        description="The total time needed from start to finish, including both prep and cooking"
    )
    servings: PositiveInt = Field(
        description="The number of people this recipe serves"
    )
    difficulty: DifficultyLevel = Field(
        description="The difficulty level of preparing this recipe"
    )
    
    # Components
    ingredients: list[Ingredient] = Field(
        description="The list of ingredients needed for this recipe"
    )
    instructions: list[Step] = Field(
        description="The ordered list of steps to prepare this recipe. Make sure to keep the order as described in the source."
    )
    
    # Additional Information
    tags: list[str] = Field(
        default_factory=list,
        description="Keywords or categories that describe this recipe, e.g., 'vegetarian', 'dessert', 'quick'"
    )
    cuisine_type: str | None = Field(
        None,
        description="The type of cuisine this recipe belongs to, e.g., 'Italian', 'Thai', 'French'"
    )
    category: MealCategory | None = Field(
        None,
        description="The category of the dish, e.g., 'main course', 'dessert', 'appetizer'"
    )