/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#8BA888', // Sage Green
                    dark: '#5F7A5E',
                    light: '#A8C3A5',
                },
                secondary: {
                    DEFAULT: '#A67B5B', // Terracotta/Brown
                    dark: '#8C6246',
                    light: '#C69D7F',
                },
                cream: '#FDFBF7', // Warm Cream Background
                olive: '#2C3E30', // Dark Olive Text
                accent: '#E07A5F', // Muted Orange/Salmon
                neutral: {
                    dark: '#2C3E30', // Using Olive as dark neutral
                    DEFAULT: '#4F5D75',
                    light: '#BFC0C0',
                    lighter: '#F2F0E9', // Slightly darker cream for contrast
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                display: ['Playfair Display', 'serif'],
            },
            boxShadow: {
                'card': '0 2px 8px rgba(0, 0, 0, 0.08)',
                'card-hover': '0 4px 16px rgba(0, 0, 0, 0.12)',
            },
            borderRadius: {
                'card': '12px',
            },
        },
    },
    plugins: [],
}
