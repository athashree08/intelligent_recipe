import React, { useState, useEffect } from 'react';
import RecipeCard from '../components/RecipeCard';

export default function SavedRecipes() {
    const [savedRecipes, setSavedRecipes] = useState([]);

    useEffect(() => {
        loadSavedRecipes();
    }, []);

    const loadSavedRecipes = () => {
        const saved = JSON.parse(localStorage.getItem('savedRecipes') || '[]');
        setSavedRecipes(saved);
    };

    const handleRemove = (recipeId) => {
        const updated = savedRecipes.filter(r => r._id !== recipeId);
        localStorage.setItem('savedRecipes', JSON.stringify(updated));
        setSavedRecipes(updated);
    };

    return (
        <div className="min-h-screen bg-neutral-lighter py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="font-display font-bold text-4xl text-neutral-dark mb-2">
                        Saved Recipes
                    </h1>
                    <p className="text-neutral">
                        Your favorite recipes in one place
                    </p>
                </div>

                {/* Recipe Grid */}
                {savedRecipes.length > 0 ? (
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {savedRecipes.map((recipe) => (
                            <div key={recipe._id} className="relative">
                                <RecipeCard recipe={recipe} showSaveButton={true} />
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-20">
                        <div className="text-8xl mb-6">❤️</div>
                        <h2 className="font-display font-semibold text-2xl text-neutral-dark mb-4">
                            No saved recipes yet
                        </h2>
                        <p className="text-neutral mb-8">
                            Start exploring and save your favorite recipes!
                        </p>
                        <a href="/recipes" className="btn-primary inline-block">
                            Browse Recipes
                        </a>
                    </div>
                )}
            </div>
        </div>
    );
}
