import os
from dotenv import load_dotenv

load_dotenv()

# Placeholder for instruction generation using LLM API
# This uses OpenAI API as an example

def generate_instructions(recipe_name, ingredients, cuisine=''):
    """
    Generate step-by-step cooking instructions using LLM
    
    Args:
        recipe_name: Name of the recipe
        ingredients: List of ingredients
        cuisine: Cuisine type (optional)
    
    Returns:
        List of instruction steps
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        # Return placeholder instructions if no API key
        return generate_placeholder_instructions(recipe_name, ingredients)
    
    try:
        import openai
        openai.api_key = api_key
        
        # Create prompt
        ingredient_list = '\n'.join([f"- {ing}" for ing in ingredients])
        prompt = f"""Generate clear, step-by-step cooking instructions for the following recipe:

Recipe Name: {recipe_name}
Cuisine: {cuisine if cuisine else 'General'}

Ingredients:
{ingredient_list}

Please provide detailed cooking instructions in a numbered list format. Be specific about cooking times, temperatures, and techniques."""

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional chef providing clear cooking instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        instructions_text = response.choices[0].message.content
        
        # Parse into list
        instructions = parse_instructions(instructions_text)
        return instructions
        
    except Exception as e:
        print(f"Error generating instructions: {e}")
        return generate_placeholder_instructions(recipe_name, ingredients)

def parse_instructions(text):
    """
    Parse instruction text into list of steps
    
    Args:
        text: Raw instruction text
    
    Returns:
        List of instruction steps
    """
    lines = text.strip().split('\n')
    instructions = []
    
    for line in lines:
        line = line.strip()
        # Remove numbering
        line = line.lstrip('0123456789.)')
        line = line.strip()
        
        if line and len(line) > 10:  # Filter out very short lines
            instructions.append(line)
    
    return instructions

def generate_placeholder_instructions(recipe_name, ingredients):
    """
    Generate simple placeholder instructions
    
    Args:
        recipe_name: Recipe name
        ingredients: List of ingredients
    
    Returns:
        List of basic instruction steps
    """
    return [
        f"Gather all ingredients for {recipe_name}.",
        "Prepare and wash all fresh ingredients.",
        "Follow standard cooking procedures for this type of dish.",
        "Combine ingredients according to the recipe requirements.",
        "Cook at appropriate temperature until done.",
        "Season to taste and serve hot."
    ]

def enhance_recipe_with_instructions(recipe):
    """
    Add generated instructions to a recipe if missing
    
    Args:
        recipe: Recipe dictionary
    
    Returns:
        Recipe with instructions added
    """
    if recipe.get('instructions'):
        return recipe
    
    # Extract ingredients
    ingredients = []
    if isinstance(recipe.get('ingredients'), list):
        for ing in recipe['ingredients']:
            if isinstance(ing, dict):
                ingredients.append(ing.get('name', ''))
            else:
                ingredients.append(str(ing))
    
    # Generate instructions
    instructions = generate_instructions(
        recipe.get('name', 'Recipe'),
        ingredients,
        recipe.get('cuisine', '')
    )
    
    recipe['instructions'] = instructions
    return recipe
