import React, { useState } from 'react';

export default function ManualIngredientInput({ onSearch }) {
    const [ingredients, setIngredients] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [suggestions] = useState([
        'tomato', 'onion', 'garlic', 'chicken', 'beef', 'pasta', 'rice',
        'cheese', 'milk', 'eggs', 'butter', 'flour', 'sugar', 'salt',
        'pepper', 'olive oil', 'carrot', 'potato', 'bell pepper', 'mushroom',
        'spinach', 'broccoli', 'lettuce', 'cucumber', 'lemon', 'ginger',
        'soy sauce', 'vinegar', 'honey', 'basil', 'oregano', 'thyme'
    ]);
    const [filteredSuggestions, setFilteredSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);

    const handleInputChange = (e) => {
        const value = e.target.value;
        setInputValue(value);

        if (value.trim()) {
            const filtered = suggestions.filter(item =>
                item.toLowerCase().includes(value.toLowerCase()) &&
                !ingredients.includes(item)
            );
            setFilteredSuggestions(filtered);
            setShowSuggestions(true);
        } else {
            setShowSuggestions(false);
        }
    };

    const addIngredient = (ingredient) => {
        const trimmed = ingredient.trim().toLowerCase();
        if (trimmed && !ingredients.includes(trimmed)) {
            setIngredients([...ingredients, trimmed]);
            setInputValue('');
            setShowSuggestions(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (inputValue.trim()) {
                addIngredient(inputValue);
            }
        }
    };

    const removeIngredient = (ingredient) => {
        setIngredients(ingredients.filter(item => item !== ingredient));
    };

    const handleSearch = () => {
        if (ingredients.length > 0) {
            onSearch(ingredients);
        }
    };

    return (
        <div className="space-y-4">
            {/* Input Field */}
            <div className="relative">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={handleInputChange}
                        onKeyPress={handleKeyPress}
                        placeholder="Type an ingredient (e.g., tomato, chicken)..."
                        className="flex-1 px-4 py-3 border border-neutral-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                    />
                    <button
                        onClick={() => addIngredient(inputValue)}
                        disabled={!inputValue.trim()}
                        className="px-6 py-3 bg-secondary text-white rounded-lg hover:bg-secondary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        Add
                    </button>
                </div>

                {/* Autocomplete Suggestions */}
                {showSuggestions && filteredSuggestions.length > 0 && (
                    <div className="absolute z-10 w-full mt-1 bg-white border border-neutral-light rounded-lg shadow-lg max-h-48 overflow-y-auto">
                        {filteredSuggestions.slice(0, 8).map((suggestion, index) => (
                            <button
                                key={index}
                                onClick={() => addIngredient(suggestion)}
                                className="w-full text-left px-4 py-2 hover:bg-neutral-lighter transition-colors"
                            >
                                {suggestion}
                            </button>
                        ))}
                    </div>
                )}
            </div>

            {/* Ingredient Tags */}
            {ingredients.length > 0 && (
                <div className="flex flex-wrap gap-2">
                    {ingredients.map((ingredient, index) => (
                        <div
                            key={index}
                            className="flex items-center gap-2 px-3 py-2 bg-primary/10 text-primary rounded-full"
                        >
                            <span className="font-medium">{ingredient}</span>
                            <button
                                onClick={() => removeIngredient(ingredient)}
                                className="hover:text-primary-dark transition-colors"
                            >
                                ✕
                            </button>
                        </div>
                    ))}
                </div>
            )}

            {/* Search Button */}
            <button
                onClick={handleSearch}
                disabled={ingredients.length === 0}
                className="btn-primary w-full text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
                🔍 Search Recipes ({ingredients.length} ingredient{ingredients.length !== 1 ? 's' : ''})
            </button>

            {/* Quick Add Suggestions */}
            {ingredients.length === 0 && (
                <div className="mt-4">
                    <p className="text-sm text-neutral mb-2">Quick add:</p>
                    <div className="flex flex-wrap gap-2">
                        {suggestions.slice(0, 10).map((suggestion, index) => (
                            <button
                                key={index}
                                onClick={() => addIngredient(suggestion)}
                                className="px-3 py-1 text-sm bg-neutral-lighter text-neutral-dark rounded-full hover:bg-primary/10 hover:text-primary transition-colors"
                            >
                                + {suggestion}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
