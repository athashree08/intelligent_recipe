import React from 'react';
import { Link } from 'react-router-dom';

export default function RecipeCard({ recipe, showSaveButton = true }) {
    const [isSaved, setIsSaved] = React.useState(false);

    React.useEffect(() => {
        const saved = JSON.parse(localStorage.getItem('savedRecipes') || '[]');
        setIsSaved(saved.some(r => r._id === recipe._id));
    }, [recipe._id]);

    const toggleSave = () => {
        const saved = JSON.parse(localStorage.getItem('savedRecipes') || '[]');

        if (isSaved) {
            const updated = saved.filter(r => r._id !== recipe._id);
            localStorage.setItem('savedRecipes', JSON.stringify(updated));
            setIsSaved(false);
        } else {
            saved.push(recipe);
            localStorage.setItem('savedRecipes', JSON.stringify(saved));
            setIsSaved(true);
        }
    };

    const matchPercentage = recipe.match_score
        ? Math.round(recipe.match_score * 100)
        : recipe.hybrid_score
            ? Math.round(recipe.hybrid_score * 100)
            : 0;

    return (
        <div className="bg-white rounded-[24px] shadow-sm hover:shadow-xl transition-all duration-300 group border border-stone-100 overflow-hidden">
            {/* Image */}
            <div className="relative h-56 bg-stone-100 overflow-hidden">
                {recipe.image_url ? (
                    <img
                        src={recipe.image_url}
                        alt={recipe.name}
                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                    />
                ) : (
                    <div className="absolute inset-0 flex items-center justify-center text-6xl opacity-50">
                        🍽️
                    </div>
                )}
                {matchPercentage > 0 && (
                    <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm text-olive px-3 py-1 rounded-full text-sm font-semibold border border-stone-100 shadow-sm">
                        {matchPercentage}% Match
                    </div>
                )}
                {showSaveButton && (
                    <button
                        onClick={toggleSave}
                        className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm p-2 rounded-full transition-colors hover:bg-white shadow-sm"
                    >
                        <span className="text-xl">{isSaved ? '❤️' : '🤍'}</span>
                    </button>
                )}
            </div>

            {/* Content */}
            <div className="p-6">
                <h3 className="font-display font-bold text-xl text-olive mb-2 line-clamp-1 group-hover:text-primary transition-colors">
                    {recipe.name}
                </h3>

                <div className="flex items-center gap-4 text-sm text-olive/70 mb-4 font-light">
                    <span className="flex items-center gap-1.5">
                        <span>🌍</span>
                        {recipe.cuisine}
                    </span>
                    <span className="flex items-center gap-1.5">
                        <span>⏱️</span>
                        {recipe.cooking_time} min
                    </span>
                </div>

                <div className="flex items-center gap-2 mb-6">
                    <span className="text-xs bg-stone-100 text-olive/80 px-2.5 py-1 rounded-full font-medium">
                        {recipe.dietary_type}
                    </span>
                </div>

                <Link
                    to={`/recipe/${recipe._id}`}
                    className="block w-full text-center bg-primary text-white font-medium py-3 rounded-xl transition-all hover:bg-primary-dark shadow-sm hover:shadow-md"
                >
                    View Recipe
                </Link>
            </div>
        </div>
    );
}
