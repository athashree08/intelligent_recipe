import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import RecipeCard from '../components/RecipeCard';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export default function RecipeList() {
    const location = useLocation();
    const detectedIngredients = location.state?.detectedIngredients || [];
    const rawOCRText = location.state?.rawText || '';
    const mode = location.state?.mode || '';

    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        cuisine: '',
        dietary_type: '',
        max_time: ''
    });
    const [filterOptions, setFilterOptions] = useState({
        cuisines: [],
        dietary_types: []
    });
    const [showOCRText, setShowOCRText] = useState(false);

    useEffect(() => {
        fetchFilterOptions();
        fetchRecipes();
    }, []);

    const fetchRecipes = async () => {
        try {
            // Check if recipes are already provided (from dish search or manual search)
            if (location.state?.recipes) {
                setRecipes(location.state.recipes);
                setLoading(false);
                return;
            }

            let url = `${API_URL}/api/recipes`;

            if (detectedIngredients.length > 0) {
                const ingredientNames = detectedIngredients.map(ing => ing.name);
                const response = await axios.post(`${API_URL}/api/recipes/recommend`, {
                    ingredients: ingredientNames
                });
                setRecipes(response.data.recipes || []);
            } else {
                const response = await axios.get(url);
                setRecipes(response.data.recipes || []);
            }
        } catch (error) {
            console.error('Error fetching recipes:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchFilterOptions = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/recipes/filter-options`);
            setFilterOptions({
                cuisines: response.data.cuisines || [],
                dietary_types: response.data.dietary_types || []
            });
        } catch (error) {
            console.error('Error fetching filter options:', error);
        }
    };

    const applyFilters = async () => {
        try {
            setLoading(true);
            const params = new URLSearchParams();
            if (filters.cuisine) params.append('cuisine', filters.cuisine);
            if (filters.dietary_type) params.append('dietary_type', filters.dietary_type);
            if (filters.max_time) params.append('max_time', filters.max_time);

            const response = await axios.get(`${API_URL}/api/recipes?${params}`);
            setRecipes(response.data.recipes || []);
        } catch (error) {
            console.error('Error applying filters:', error);
        } finally {
            setLoading(false);
        }
    };

    // Get related data from location state
    const searchedIngredients = location.state?.searchedIngredients || [];

    return (
        <div className="min-h-screen bg-neutral-lighter py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="font-display font-bold text-4xl text-neutral-dark mb-4">
                        {mode === 'manual' && searchedIngredients.length > 0
                            ? 'Recipe Recommendations'
                            : detectedIngredients.length > 0
                                ? 'Recipe Recommendations'
                                : 'All Recipes'}
                    </h1>

                    {/* Display detected ingredients */}
                    {detectedIngredients.length > 0 && mode === 'ingredients' && (
                        <div className="flex flex-wrap gap-2 mb-4">
                            <span className="text-neutral">Detected ingredients:</span>
                            {detectedIngredients.map((ing, idx) => (
                                <span key={idx} className="ingredient-chip">
                                    {ing.name}
                                    {ing.confidence && (
                                        <span className="text-xs opacity-75">
                                            {Math.round(ing.confidence * 100)}%
                                        </span>
                                    )}
                                </span>
                            ))}
                        </div>
                    )}

                    {/* Display manually searched ingredients */}
                    {searchedIngredients.length > 0 && mode === 'manual' && (
                        <div className="flex flex-wrap gap-2 mb-4">
                            <span className="text-neutral">Searched ingredients:</span>
                            {searchedIngredients.map((ing, idx) => (
                                <span key={idx} className="ingredient-chip">
                                    {ing}
                                </span>
                            ))}
                        </div>
                    )}

                    {/* Display OCR extracted text */}
                    {rawOCRText && mode === 'ocr' && (
                        <div className="mb-6 bg-white rounded-lg p-4 border border-neutral-light">
                            <button
                                onClick={() => setShowOCRText(!showOCRText)}
                                className="flex items-center justify-between w-full text-left"
                            >
                                <span className="font-semibold text-neutral-dark">
                                    📄 Extracted Text from Label
                                </span>
                                <span className="text-2xl">{showOCRText ? '▼' : '▶'}</span>
                            </button>
                            {showOCRText && (
                                <div className="mt-4 p-4 bg-neutral-lighter rounded-lg">
                                    <pre className="text-sm text-neutral whitespace-pre-wrap font-mono">
                                        {rawOCRText}
                                    </pre>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Display detected ingredients from OCR */}
                    {detectedIngredients.length > 0 && mode === 'ocr' && (
                        <div className="flex flex-wrap gap-2 mb-4">
                            <span className="text-neutral">Extracted ingredients:</span>
                            {detectedIngredients.map((ing, idx) => (
                                <span key={idx} className="ingredient-chip">
                                    {ing.name}
                                </span>
                            ))}
                        </div>
                    )}


                </div>

                {/* Filters */}
                <div className="card p-6 mb-8">
                    <h2 className="font-semibold text-lg mb-4">Filters</h2>
                    <div className="grid md:grid-cols-4 gap-4">
                        <select
                            value={filters.cuisine}
                            onChange={(e) => setFilters({ ...filters, cuisine: e.target.value })}
                            className="px-4 py-2 border border-neutral-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                        >
                            <option value="">All Cuisines</option>
                            {filterOptions.cuisines.map((cuisine) => (
                                <option key={cuisine} value={cuisine}>{cuisine}</option>
                            ))}
                        </select>

                        <select
                            value={filters.dietary_type}
                            onChange={(e) => setFilters({ ...filters, dietary_type: e.target.value })}
                            className="px-4 py-2 border border-neutral-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                        >
                            <option value="">All Dietary Types</option>
                            {filterOptions.dietary_types.map((type) => (
                                <option key={type} value={type}>{type}</option>
                            ))}
                        </select>

                        <input
                            type="number"
                            placeholder="Max cooking time (min)"
                            value={filters.max_time}
                            onChange={(e) => setFilters({ ...filters, max_time: e.target.value })}
                            className="px-4 py-2 border border-neutral-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                        />

                        <button onClick={applyFilters} className="btn-primary">
                            Apply Filters
                        </button>
                    </div>
                </div>

                {/* Recipe Grid */}
                {loading ? (
                    <div className="text-center py-20">
                        <div className="text-6xl mb-4 animate-bounce">🍳</div>
                        <p className="text-xl text-neutral">Loading delicious recipes...</p>
                    </div>
                ) : recipes.length > 0 ? (
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {recipes.map((recipe) => (
                            <RecipeCard key={recipe._id} recipe={recipe} />
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-20">
                        <div className="text-6xl mb-4">😕</div>
                        <p className="text-xl text-neutral">No recipes found</p>
                    </div>
                )}
            </div>
        </div>
    );
}
