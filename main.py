from fasthtml.common import *
from monsterui.core import *
import json


app, rt = fast_app(hdrs=Theme.slate.headers())


def format_time(iso_duration):
    if not iso_duration:
        return ""
    hours = 0
    minutes = 0
    if 'H' in iso_duration:
        hours = int(iso_duration.split('H')[0].replace('PT', ''))
    if 'M' in iso_duration:
        minutes = int(iso_duration.split('M')[0].split('H')[-1])
    
    time_str = []
    if hours:
        time_str.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes:
        time_str.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    return " ".join(time_str)

def create_ingredient_list(ingredients):
    return Ul(
        *[Li(
            Div(
                Div(f"{ing['quantity']} {ing['unit']}", cls="text-sm text-gray-600"),
                Div(ing['name'], cls="font-medium"),
                P(ing['notes'], cls="text-sm text-gray-500") if ing['notes'] else "",
                cls="flex flex-col"
            ),
            cls="p-2 border-b"
        ) for ing in ingredients],
        cls="divide-y rounded-lg bg-card"
    )

def create_instructions_list(instructions):
    return Ol(
        *[Li(
            Article(
                P(instruction['instruction'], cls="text-base"),
                P(instruction['note'], cls="text-sm text-gray-500 mt-1") if instruction['note'] else "",
                cls="p-2"
            ),
            cls="mb-2"
        ) for instruction in instructions],
        cls="space-y-1"
    )

def difficulty_to_stars(difficulty):
    stars = {
        'easy': '★☆☆',
        'medium': '★★☆',
        'hard': '★★★'
    }
    return stars.get(difficulty.lower(), '☆☆☆')

@rt('/')
def get():
    with open('otto.json', 'r') as f:
        recipe = json.loads(f.read())
    
    return Div(
        Article(
            # Header section
            Header(
                H1(recipe['title'], cls="text-3xl font-bold mb-2"),
                P(recipe['description'], cls="text-gray-600 italic"),
                cls="mb-3"
            ),
            
            # Recipe metadata
            Section(
                Grid(
                    Div(
                        H3("Author", cls="text-sm font-medium text-gray-500"),
                        P(recipe['author'], cls="mt-0.5"),
                        cls="p-2"
                    ),
                    Div(
                        H3("Difficulty", cls="text-sm font-medium text-gray-500"),
                        P(difficulty_to_stars(recipe['difficulty']), cls="mt-0.5"),
                        cls="p-2"
                    ),
                    Div(
                        H3("Servings", cls="text-sm font-medium text-gray-500"),
                        P(str(recipe['servings']), cls="mt-0.5"),
                        cls="p-2"
                    ),
                    Div(
                        H3("Prep Time", cls="text-sm font-medium text-gray-500"),
                        P(
                            UkIcon("clock", cls="inline-block w-4 h-4 mr-1"),
                            format_time(recipe['prep_time']),
                            cls="mt-0.5 flex items-center"
                        ),
                        cls="p-2"
                    ),
                    Div(
                        H3("Cook Time", cls="text-sm font-medium text-gray-500"),
                        P(
                            UkIcon("clock", cls="inline-block w-4 h-4 mr-1"),
                            format_time(recipe['cook_time']),
                            cls="mt-0.5 flex items-center"
                        ),
                        cls="p-2"
                    ),
                    Div(
                        H3("Total Time", cls="text-sm font-medium text-gray-500"),
                        P(
                            UkIcon("clock", cls="inline-block w-4 h-4 mr-1"),
                            format_time(recipe['total_time']),
                            cls="mt-0.5 flex items-center"
                        ),
                        cls="p-2"
                    ),
                    cls="grid-cols-2 md:grid-cols-3 gap-2 bg-muted rounded-lg"
                ),
                cls="mb-3 py-4"
            ),
            
            # Main content
            Grid(
                # Ingredients section
                Section(
                    H2("Ingredients", cls="text-xl font-semibold mb-2"),
                    create_ingredient_list(recipe['ingredients']),
                    cls="py-2"
                ),
                
                # Instructions section
                Section(
                    H2("Instructions", cls="text-xl font-semibold mb-2"),
                    create_instructions_list(recipe['instructions']),
                    cls="py-2"
                ),
                cls="grid-cols-1 lg:grid-cols-2 gap-4"
            ),
            
            # Footer with tags
            Footer(
                H3("Tags", cls="text-base font-semibold mb-1"),
                Div(
                    *[Span(tag, cls="inline-block px-2 py-0.5 rounded-full text-sm font-medium bg-primary/10 text-primary mr-1 mb-1") for tag in recipe['tags']],
                    cls="flex flex-wrap"
                ),
                cls="mt-4 pt-4 border-t"
            ),
            
            cls="max-w-4xl mx-auto p-10 bg-background rounded-xl shadow-lg"
        ),
        cls="min-h-screen bg-muted p-2 md:p-4"
    )

serve()