# 🍳 Intelligent Recipe Generator

An AI-powered recipe recommendation system that uses computer vision and machine learning to detect ingredients from images and suggest personalized recipes.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![React](https://img.shields.io/badge/React-18.2-61dafb)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green)

## ✨ Features

### 🤖 AI Ingredient Detection
- **93% accuracy** ingredient recognition using MobileNetV2
- Trained on 10 common ingredients: apple, banana, tomato, onion, potato, carrot, cucumber, orange, lemon, corn
- Real-time image processing and prediction

### 📝 OCR for Packaged Foods
- Extract ingredient lists from food package labels using Tesseract OCR
- Automatic text parsing and ingredient extraction
- Support for various label formats

### 🎯 Smart Recipe Recommendations
- **Primary ingredient filtering** - Shows recipes containing your highest-confidence detected ingredient
- Hybrid recommendation system (90% ingredient match + 10% content similarity)
- Deduplication and relevance filtering
- 81 professional recipes from TheMealDB API

### 🎨 Modern Food-Centric UI
- Zomato/Swiggy-inspired design with Tailwind CSS
- Warm color palette (oranges, reds, neutrals)
- Fully responsive (mobile, tablet, desktop)
- Real food photography from TheMealDB
- Save/unsave recipes with localStorage persistence
- Recipe rating system (1-5 stars)

## 🏗️ Architecture

### Backend (Flask + Python)
```
backend/
├── app.py                          # Flask application entry point
├── models/
│   ├── ingredient_recognition.py  # MobileNetV2 model wrapper
│   ├── train_subset.py            # Model training script
│   └── database.py                # MongoDB interface
├── routes/
│   ├── auth_routes.py             # JWT authentication
│   ├── image_routes.py            # Image upload & processing
│   └── recipe_routes.py           # Recipe CRUD & recommendations
├── utils/
│   ├── ingredient_matcher.py      # Fuzzy ingredient matching
│   ├── recommendation_engine.py   # Hybrid recommendation algorithm
│   ├── ocr_processor.py           # Tesseract OCR integration
│   └── image_preprocessing.py     # Image preprocessing pipeline
└── fetch_mealdb_recipes.py        # TheMealDB API integration
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx             # Navigation bar
│   │   └── RecipeCard.jsx         # Recipe card component
│   ├── pages/
│   │   ├── Home.jsx               # Landing page
│   │   ├── Upload.jsx             # Image upload (ML + OCR modes)
│   │   ├── RecipeList.jsx         # Recipe grid with filters
│   │   ├── RecipeDetail.jsx       # Full recipe view
│   │   ├── SavedRecipes.jsx       # Bookmarked recipes
│   │   └── Login.jsx              # Authentication
│   ├── context/
│   │   └── AuthContext.jsx        # Auth state management
│   └── index.css                  # Tailwind + custom styles
└── tailwind.config.js             # Design system configuration
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB 6.0+
- Tesseract OCR (for OCR features)

### Installation

#### 1. Clone Repository
```bash
git clone <repository-url>
cd intelligent_recipe
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and JWT secret

# Download trained model
# Place model files in backend/models/saved_models/
```

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 4. Install Tesseract OCR (Optional)
**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR\`
3. Path is already configured in `ocr_processor.py`

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

### Running the Application

#### Start Backend
```bash
cd backend
venv\Scripts\activate
python app.py
```
Backend runs on: **http://localhost:5000**

#### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on: **http://localhost:5173**

## 📖 Usage

### 1. AI Ingredient Detection
1. Navigate to **Upload** page
2. Select **🤖 AI Detection** mode
3. Upload photo of fresh ingredient (e.g., banana)
4. View recipes containing that ingredient

### 2. OCR for Packaged Foods
1. Navigate to **Upload** page
2. Select **📝 OCR (Labels)** mode
3. Upload photo of food package ingredient list
4. View recipes using extracted ingredients

### 3. Browse Recipes
- View all 81 professional recipes
- Filter by cuisine, dietary type, cooking time
- Save favorites for later
- Rate recipes (1-5 stars)

### 4. Recipe Details
- View full recipe with hero image
- See ingredients list
- Follow step-by-step instructions
- Check nutritional information

## 🎯 Model Performance

### Ingredient Recognition Model
- **Architecture:** MobileNetV2 (transfer learning)
- **Training Strategy:** Two-phase training
  - Phase 1: Train top layers (10 epochs)
  - Phase 2: Fine-tune last 20 layers (40 epochs)
- **Validation Accuracy:** 93%
- **Dataset:** Kaggle Fruit and Vegetable Image Recognition (subset)
- **Trained Ingredients:** apple, banana, tomato, onion, potato, carrot, cucumber, orange, lemon, corn

### Recommendation Algorithm
- **Primary Ingredient Filtering:** Shows only recipes containing highest-confidence ingredient
- **Hybrid Scoring:** 90% ingredient match + 10% content similarity (TF-IDF)
- **Deduplication:** Removes duplicate recipes by name
- **Relevance Threshold:** Filters out low-match recipes

## 🗄️ Database Schema

### Recipes Collection
```javascript
{
  name: String,
  cuisine: String,
  dietary_type: String,
  cooking_time: Number,
  ingredients: [{
    name: String,
    quantity: String,
    unit: String
  }],
  instructions: [String],
  image_url: String,  // TheMealDB image
  nutrition: {
    calories: Number,
    protein: Number,
    carbs: Number,
    fats: Number
  }
}
```

### Users Collection
```javascript
{
  username: String (unique),
  email: String (unique),
  password: String (hashed),
  created_at: Date
}
```

## 🎨 Design System

### Color Palette
- **Primary:** `#FF6B35` (warm orange)
- **Secondary:** `#F7931E` (golden)
- **Accent:** `#C1121F` (red)
- **Neutral:** `#2D3142` to `#F8F9FA`

### Typography
- **Headings:** Poppins (bold, display)
- **Body:** Inter (clean, readable)

### Components
- Modern recipe cards with real food photography
- Responsive grid layouts
- Smooth transitions and hover effects
- Glassmorphism and subtle shadows

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Image Processing
- `POST /api/image/recognize` - AI ingredient detection
- `POST /api/image/ocr` - OCR ingredient extraction

### Recipes
- `GET /api/recipes` - Get all recipes
- `GET /api/recipes/:id` - Get recipe details
- `POST /api/recipes/recommend` - Get recommendations
- `GET /api/recipes/search` - Search with filters

## 🔧 Configuration

### Environment Variables (.env)
```env
# MongoDB
MONGO_URI=mongodb://localhost:27017/intelligent_recipe

# JWT
JWT_SECRET_KEY=your-secret-key-here

# Flask
FLASK_DEBUG=True
MAX_CONTENT_LENGTH=5242880  # 5MB

# Upload
UPLOAD_FOLDER=uploads
```

### Tailwind Config
Custom design tokens in `frontend/tailwind.config.js`:
- Colors, fonts, shadows, border radius
- Responsive breakpoints
- Custom component classes

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

See `INTERNSHIP_OPTIMIZATION.md` for detailed deployment guides:
- Heroku deployment
- AWS deployment
- Docker containerization
- CI/CD with GitHub Actions

## 🤝 Contributing

This is an academic project. For improvements:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📝 License

This project is for educational purposes.

## 👥 Authors

- **Athashree** - Initial work and development

## 🙏 Acknowledgments

- **TheMealDB** - Recipe data and images
- **Kaggle** - Fruit and Vegetable dataset
- **MobileNetV2** - Pre-trained model
- **Tesseract OCR** - Text extraction
- **Tailwind CSS** - UI framework

## 📞 Support

For issues or questions:
- Create an issue in the repository
- Check `INTERNSHIP_OPTIMIZATION.md` for deployment help

---

**Built with ❤️ for intelligent recipe recommendations**
