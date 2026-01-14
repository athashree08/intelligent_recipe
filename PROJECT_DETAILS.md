# Project Technical Documentation

## 1. Project Structure Overview

The project is a full-stack web application with a clear separation of concerns between the Frontend (React/Vite) and Backend (Flask/Python).

### **Backend (`/backend`)**
*   **`app.py`**: The entry point of the Flask application. Initializes the app, database connection, and registers blueprints.
*   **`routes/`**: Contains the API endpoint definitions.
    *   `recipe_routes.py`: Logic for listing, searching, recommending, and retrieving recipes.
    *   `auth_routes.py`: User authentication (Login/Signup) logic using JWT.
    *   `image_routes.py`: Handles image uploads and triggers the recognition model.
*   **`models/`**: Stores machine learning models and database schemas.
    *   `ingredient_model.h5`: The trained Keras model for ingredient recognition.
    *   `train_model.py`: Script used to train the MobileNetV2-based model.
    *   `database.py`: MongoDB connection and helper functions.
*   **`utils/`**: Helper utilities.
    *   `nutrition_api.py`: Integrates with USDA FoodData Central for nutritional analysis.
    *   `ocr_processor.py`: Backup/Secondary logic for OCR (Tesseract) if needed.
    *   `recommendation_engine.py`: Logic to match ingredients to recipes (Hybrid/Content-based).
*   **`image_processing/`**: Core vision logic.
    *   `ingredient_recognition.py`: wrapper class for loading and predicting with the `.h5` model.
    *   `ocr.py`: OCR utility functions.

### **Frontend (`/frontend`)**
*   **`src/pages/`**:
    *   `Home.jsx`: The organic landing page and user dashboard.
    *   `Upload.jsx`: Interface for capturing/uploading photos and seeing results.
    *   `RecipeList.jsx`: Displays generated or searched recipes.
    *   `RecipeDetail.jsx`: Full view of a recipe with nutrition and instructions.
*   **`src/components/`**: Reusable UI components (`Navbar`, `RecipeCard`, `ImageUpload`).
*   **`src/services/api.js`**: Axios configuration for communicating with the backend APIs.
*   **`tailwind.config.js`**: Configuration for the "La Petite Cuisine" theme (Sage/Cream colors).

---

## 2. API Endpoints

### **Recipes (`/api/recipes`)**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | List all recipes. Supports filtering by `cuisine`, `dietary_type`, `max_time`. |
| `GET` | `/search` | Search recipes with query text and filters. |
| `POST` | `/recommend` | **Core Feature**: Recommend recipes based on a list of ingredients. |
| `POST` | `/search_by_ingredients` | Search recipes for manually entered ingredients. |
| `GET` | `/<id>` | Get full details of a specific recipe. |
| `GET` | `/<id>/nutrition` | **New**: Trigger a real-time call to USDA API to calculate/update nutrition data. |

### **Authentication (`/api/auth`)**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/register` | Create a new user account. |
| `POST` | `/login` | Authenticate and receive a JWT token. |

### **Images (`/api/image`)**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/recognize` | Upload an image to detect ingredients using the AI model + OCR. |

---

## 3. AI & Machine Learning Details

### **Ingredient Recognition Model**
*   **Architecture**: **MobileNetV2** (Convolutional Neural Network)
    *   **Base**: Pre-trained on ImageNet (Transfer Learning).
    *   **Head**: Custom dense layers added for specific ingredient classification.
*   **Training Strategy**:
    *   **Phase 1**: Frozen base layers, trained top layers only (warmup).
    *   **Phase 2**: Fine-tuning the top 20 layers of MobileNetV2 with a lower learning rate.
*   **Augmentation**: Rotation (20°), Width/Height Shift (0.2), Horizontal Flip, Zoom (0.2).
*   **Input Size**: 224x224 pixels.
*   **Optimization**: Adam optimizer, Early Stopping (monitor `val_loss`), ReduceLROnPlateau.

### **Recipe Recommendation Engine**
*   **Hybrid Approach**: Combines keyword matching (finding recipes containing the ingredients) with semantic understanding.
*   **OpenAI Integration**: Uses `gpt-3.5-turbo` to:
    *   Generate coherent cooking instructions if missing.
    *   Fill in missing metadata (cuisine, tags).

---

## 4. External Services & APIs

### **1. USDA FoodData Central**
*   **Purpose**: Calculating accurate nutritional information.
*   **Key Features**:
    *   "Fresh" vs "Packaged" filtering to prefer raw ingredients (e.g., "Raw Banana" vs "Banana Chips").
    *   **Unit Parsing**: Intelligent regex parsing to understand "1 large egg", "25g butter", etc.
    *   **Nutrients**: Extracts Energy (kcal), Protein, Fat, Carbohydrates.

### **2. OpenAI (GPT-3.5)**
*   **Purpose**: Content generation.
*   **Why**: To turn a simple list of ingredients into a structured, step-by-step cooking guide.

### **3. MongoDB (Database)**
*   **Role**: Primary data store.
*   **Collections**: `users` (auth), `recipes` (content), `ingredients` (cache).

---

## 5. Deployment & Execution
*   **Environment**: Uses `.env` for secrets (`OPENAI_API_KEY`, `USDA_API_KEY`, etc.).
*   **Run**:
    *   Backend: `python app.py` (Runs on Port 5000)
    *   Frontend: `npm run dev` (Runs on Port 5173 with Vite)
