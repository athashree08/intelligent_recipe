import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export default function RecipeDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [recipe, setRecipe] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isSaved, setIsSaved] = useState(false);
    const [userRating, setUserRating] = useState(0);
    const [calculatingNutrition, setCalculatingNutrition] = useState(false);

    useEffect(() => {
        fetchRecipe();
        checkIfSaved();
    }, [id]);

    const fetchRecipe = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/recipes/${id}`);
            setRecipe(response.data.recipe);
        } catch (error) {
            console.error('Error fetching recipe:', error);
        } finally {
            setLoading(false);
        }
    };

    const checkIfSaved = () => {
        const saved = JSON.parse(localStorage.getItem('savedRecipes') || '[]');
        setIsSaved(saved.some(r => r._id === id));
    };

    const toggleSave = () => {
        const saved = JSON.parse(localStorage.getItem('savedRecipes') || '[]');

        if (isSaved) {
            const updated = saved.filter(r => r._id !== id);
            localStorage.setItem('savedRecipes', JSON.stringify(updated));
            setIsSaved(false);
        } else {
            saved.push(recipe);
            localStorage.setItem('savedRecipes', JSON.stringify(saved));
            setIsSaved(true);
        }
    };

    const calculateNutrition = async () => {
        setCalculatingNutrition(true);
        try {
            const response = await axios.get(`${API_URL}/api/recipes/${id}/nutrition`);
            // Update recipe with calculated nutrition
            setRecipe(prev => ({
                ...prev,
                nutrition: response.data.nutrition
            }));
        } catch (error) {
            console.error('Error calculating nutrition:', error);
            alert(error.response?.data?.message || 'Failed to calculate nutrition');
        } finally {
            setCalculatingNutrition(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-neutral-lighter flex items-center justify-center">
                <div className="text-center">
                    <div className="text-6xl mb-4 animate-bounce">🍳</div>
                    <p className="text-xl text-neutral">Loading recipe...</p>
                </div>
            </div>
        );
    }

    if (!recipe) {
        return (
            <div className="min-h-screen bg-neutral-lighter flex items-center justify-center">
                <div className="text-center">
                    <div className="text-6xl mb-4">😕</div>
                    <p className="text-xl text-neutral mb-4">Recipe not found</p>
                    <button onClick={() => navigate('/recipes')} className="btn-primary">
                        Browse Recipes
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-neutral-lighter">
            {/* Hero Image */}
            <div className="relative h-96 bg-gradient-to-br from-primary/30 to-secondary/30 overflow-hidden">
                {recipe.image_url ? (
                    <img
                        src={recipe.image_url}
                        alt={recipe.name}
                        className="w-full h-full object-cover"
                    />
                ) : (
                    <div className="absolute inset-0 flex items-center justify-center text-9xl">
                        🍽️
                    </div>
                )}
                <button
                    onClick={() => navigate(-1)}
                    className="absolute top-6 left-6 bg-white/90 hover:bg-white px-4 py-2 rounded-lg transition-colors"
                >
                    ← Back
                </button>
                <button
                    onClick={toggleSave}
                    className="absolute top-6 right-6 bg-white/90 hover:bg-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
                >
                    <span className="text-2xl">{isSaved ? '❤️' : '🤍'}</span>
                    <span className="font-medium">{isSaved ? 'Saved' : 'Save Recipe'}</span>
                </button>
            </div>

            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 -mt-20">
                {/* Recipe Card */}
                <div className="card p-8 mb-8">
                    <h1 className="font-display font-bold text-4xl text-neutral-dark mb-4">
                        {recipe.name}
                    </h1>

                    <div className="flex flex-wrap gap-4 mb-6">
                        <span className="flex items-center gap-2 text-neutral">
                            <span className="text-2xl">🌍</span>
                            <span className="font-medium">{recipe.cuisine}</span>
                        </span>
                        <span className="flex items-center gap-2 text-neutral">
                            <span className="text-2xl">⏱️</span>
                            <span className="font-medium">{recipe.cooking_time} minutes</span>
                        </span>
                        <span className="flex items-center gap-2 text-neutral">
                            <span className="text-2xl">🥗</span>
                            <span className="font-medium">{recipe.dietary_type}</span>
                        </span>
                    </div>

                    {/* Rating */}
                    <div className="mb-8">
                        <p className="text-sm text-neutral mb-2">Rate this recipe:</p>
                        <div className="flex gap-2">
                            {[1, 2, 3, 4, 5].map((star) => (
                                <button
                                    key={star}
                                    onClick={() => setUserRating(star)}
                                    className="text-3xl transition-transform hover:scale-110"
                                >
                                    {star <= userRating ? '⭐' : '☆'}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Ingredients */}
                <div className="card p-8 mb-8">
                    <h2 className="font-display font-semibold text-2xl text-neutral-dark mb-6">
                        Ingredients
                    </h2>
                    <div className="grid md:grid-cols-2 gap-4">
                        {recipe.ingredients?.map((ing, idx) => (
                            <div key={idx} className="flex items-center gap-3 p-3 bg-neutral-lighter rounded-lg">
                                <span className="text-2xl">🥕</span>
                                <div>
                                    <p className="font-medium text-neutral-dark">{ing.name}</p>
                                    <p className="text-sm text-neutral">
                                        {ing.quantity} {ing.unit}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Instructions */}
                <div className="card p-8 mb-8">
                    <h2 className="font-display font-semibold text-2xl text-neutral-dark mb-6">
                        Instructions
                    </h2>
                    <div className="space-y-4">
                        {recipe.instructions?.map((step, idx) => (
                            <div key={idx} className="flex gap-4">
                                <div className="flex-shrink-0 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-semibold">
                                    {idx + 1}
                                </div>
                                <p className="text-neutral-dark pt-1">{step}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Nutrition - Show if data exists or allow calculation */}
                <div className="card p-8 mb-8">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="font-display font-semibold text-2xl text-neutral-dark">
                            Nutritional Information
                        </h2>
                        {recipe.nutrition && (recipe.nutrition.calories > 0 || recipe.nutrition.protein > 0) ? (
                            <button
                                onClick={calculateNutrition}
                                disabled={calculatingNutrition}
                                className="btn-secondary text-sm"
                            >
                                {calculatingNutrition ? '⏳ Recalculating...' : '🔄 Recalculate'}
                            </button>
                        ) : (
                            <button
                                onClick={calculateNutrition}
                                disabled={calculatingNutrition}
                                className="btn-secondary"
                            >
                                {calculatingNutrition ? (
                                    <span className="flex items-center gap-2">
                                        <span className="animate-spin">⏳</span>
                                        Calculating...
                                    </span>
                                ) : (
                                    '🔬 Calculate Nutrition'
                                )}
                            </button>
                        )}
                    </div>

                    {recipe.nutrition && (recipe.nutrition.calories > 0 || recipe.nutrition.protein > 0) ? (
                        <>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="text-center p-4 bg-neutral-lighter rounded-lg">
                                    <p className="text-3xl mb-2">🔥</p>
                                    <p className="text-2xl font-bold text-primary">{recipe.nutrition.calories}</p>
                                    <p className="text-sm text-neutral">Calories</p>
                                </div>
                                <div className="text-center p-4 bg-neutral-lighter rounded-lg">
                                    <p className="text-3xl mb-2">🥩</p>
                                    <p className="text-2xl font-bold text-primary">{recipe.nutrition.protein}g</p>
                                    <p className="text-sm text-neutral">Protein</p>
                                </div>
                                <div className="text-center p-4 bg-neutral-lighter rounded-lg">
                                    <p className="text-3xl mb-2">🍞</p>
                                    <p className="text-2xl font-bold text-primary">{recipe.nutrition.carbs}g</p>
                                    <p className="text-sm text-neutral">Carbs</p>
                                </div>
                                <div className="text-center p-4 bg-neutral-lighter rounded-lg">
                                    <p className="text-3xl mb-2">🥑</p>
                                    <p className="text-2xl font-bold text-primary">{recipe.nutrition.fats || recipe.nutrition.fat}g</p>
                                    <p className="text-sm text-neutral">Fats</p>
                                </div>
                            </div>
                            {recipe.nutrition.calculated && (
                                <p className="text-sm text-neutral mt-4 text-center">
                                    ℹ️ Calculated using USDA database ({recipe.nutrition.ingredients_matched}/{recipe.nutrition.total_ingredients} ingredients matched)
                                    <br />
                                    <strong>Note:</strong> Values shown are for the <strong>entire recipe</strong>, not per serving.
                                </p>
                            )}
                        </>
                    ) : (
                        <div className="text-center py-8 text-neutral">
                            <p className="text-4xl mb-4">📊</p>
                            <p className="mb-2">Nutritional information not available</p>
                            <p className="text-sm">Click "Calculate Nutrition" to get estimated values using USDA database</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
