import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ManualIngredientInput from '../components/ManualIngredientInput';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export default function Upload() {
    const navigate = useNavigate();
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    const [mode, setMode] = useState('ingredients'); // 'ingredients', 'ocr', or 'manual'
    const [uploadMethod, setUploadMethod] = useState('file'); // 'file' or 'camera'
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [cameraStream, setCameraStream] = useState(null);

    // Camera functions
    const startCamera = async () => {
        try {
            console.log('Starting camera...');
            console.log('Video ref exists:', !!videoRef.current);

            // Try with ideal constraints first
            let stream;
            try {
                console.log('Requesting camera with ideal constraints...');
                stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { ideal: 1280 },
                        height: { ideal: 720 },
                        facingMode: 'user' // Use front camera by default for laptops
                    }
                });
                console.log('Camera stream obtained with ideal constraints');
            } catch (err) {
                // Fallback to basic constraints if ideal fails
                console.log('Trying fallback camera constraints...', err);
                stream = await navigator.mediaDevices.getUserMedia({
                    video: true
                });
                console.log('Camera stream obtained with fallback constraints');
            }

            console.log('Stream active:', stream.active);
            console.log('Video tracks:', stream.getVideoTracks().length);

            setCameraStream(stream);
            setUploadMethod('camera');

            // Wait a tick for state to update and DOM to render
            setTimeout(() => {
                if (videoRef.current) {
                    console.log('Setting video srcObject...');
                    videoRef.current.srcObject = stream;

                    // Wait for video to be ready
                    videoRef.current.onloadedmetadata = () => {
                        console.log('Video metadata loaded, playing...');
                        console.log('Video dimensions:', videoRef.current.videoWidth, 'x', videoRef.current.videoHeight);
                        videoRef.current.play()
                            .then(() => {
                                console.log('Video playing successfully');
                                setError('');
                            })
                            .catch(err => {
                                console.error('Error playing video:', err);
                                setError('Camera initialized but playback failed. Please try again.');
                            });
                    };
                } else {
                    console.error('Video ref is null after state update');
                    setError('Camera UI not ready. Please try again.');
                }
            }, 100);

        } catch (err) {
            console.error('Camera error:', err);
            setError('Unable to access camera. Please check permissions and ensure no other app is using the camera.');
        }
    };

    const stopCamera = () => {
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            setCameraStream(null);
        }
        setUploadMethod('file');
    };

    const capturePhoto = () => {
        if (videoRef.current && canvasRef.current) {
            const canvas = canvasRef.current;
            const video = videoRef.current;

            // Ensure video has valid dimensions
            if (!video.videoWidth || !video.videoHeight) {
                setError('Camera not ready. Please wait a moment and try again.');
                return;
            }

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);

            // Convert canvas to blob with error handling
            canvas.toBlob((blob) => {
                if (!blob) {
                    setError('Failed to capture photo. Please try again.');
                    return;
                }

                try {
                    const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
                    const previewUrl = URL.createObjectURL(blob);
                    setSelectedFile(file);
                    setPreview(previewUrl);
                    stopCamera();
                    setError('');
                } catch (err) {
                    console.error('Error creating preview:', err);
                    setError('Failed to create photo preview. Please try again.');
                }
            }, 'image/jpeg', 0.95);
        }
    };

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setError('');
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setError('');
        }
    };

    const handleSubmit = async () => {
        if (!selectedFile) {
            setError('Please select an image first');
            return;
        }

        setLoading(true);
        setError('');

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post(`${API_URL}/api/image/recognize`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const ingredients = response.data.ingredients || [];
            navigate('/recipes', { state: { detectedIngredients: ingredients, mode: 'ingredients' } });
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to process image. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleOCRSubmit = async () => {
        if (!selectedFile) {
            setError('Please select an image first');
            return;
        }

        setLoading(true);
        setError('');

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post(`${API_URL}/api/image/ocr`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const ingredients = response.data.ingredients || [];
            navigate('/recipes', { state: { detectedIngredients: ingredients, mode: 'ocr', rawText: response.data.raw_text } });
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to extract text from image. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleManualSearch = async (ingredients) => {
        setLoading(true);
        setError('');

        try {
            const response = await axios.post(`${API_URL}/api/recipes/search-by-ingredients`, {
                ingredients: ingredients,
                method: 'hybrid'
            });

            const recipes = response.data.recipes || [];
            navigate('/recipes', {
                state: {
                    recipes: recipes,
                    searchedIngredients: ingredients,
                    mode: 'manual'
                }
            });
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to search recipes. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const resetUpload = () => {
        setPreview(null);
        setSelectedFile(null);
        stopCamera();
    };

    return (
        <div className="min-h-screen bg-neutral-lighter py-12">
            <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="text-6xl mb-4">
                        {mode === 'manual' ? '✍️' : mode === 'ocr' ? '📦' : '📸'}
                    </div>
                    <h1 className="font-display font-bold text-4xl text-neutral-dark mb-4">
                        {mode === 'manual' ? 'Search by Ingredients' : mode === 'ocr' ? 'Product Label Scanner' : 'Recognize Ingredients'}
                    </h1>
                    <p className="text-lg text-neutral mb-6">
                        {mode === 'manual'
                            ? 'Enter ingredients you have and discover recipes'
                            : mode === 'ocr'
                                ? 'Scan packaged food labels to extract ingredients'
                                : 'Take a photo of fresh ingredients for AI detection'}
                    </p>

                    {/* Mode Toggle */}
                    <div className="flex flex-wrap justify-center gap-3 mb-8">
                        <button
                            onClick={() => { setMode('ingredients'); resetUpload(); }}
                            className={`px-5 py-3 rounded-lg font-medium transition-colors ${mode === 'ingredients'
                                ? 'bg-primary text-white'
                                : 'bg-white text-neutral border border-neutral-light hover:border-primary'
                                }`}
                        >
                            🤖 Fresh Ingredients
                        </button>
                        <button
                            onClick={() => { setMode('ocr'); resetUpload(); }}
                            className={`px-5 py-3 rounded-lg font-medium transition-colors ${mode === 'ocr'
                                ? 'bg-primary text-white'
                                : 'bg-white text-neutral border border-neutral-light hover:border-primary'
                                }`}
                        >
                            📦 Product Label
                        </button>
                        <button
                            onClick={() => { setMode('manual'); resetUpload(); }}
                            className={`px-5 py-3 rounded-lg font-medium transition-colors ${mode === 'manual'
                                ? 'bg-primary text-white'
                                : 'bg-white text-neutral border border-neutral-light hover:border-primary'
                                }`}
                        >
                            ✍️ Manual Input
                        </button>
                    </div>
                </div>

                {/* Main Content */}
                <div className="card p-8">
                    {mode === 'manual' ? (
                        /* Manual Input Mode */
                        <ManualIngredientInput onSearch={handleManualSearch} />
                    ) : (
                        /* Image Upload/Camera Mode */
                        <>
                            {!preview && uploadMethod === 'file' && (
                                <>
                                    {/* Upload Area */}
                                    <div
                                        onDrop={handleDrop}
                                        onDragOver={(e) => e.preventDefault()}
                                        className="border-2 border-dashed border-neutral-light rounded-card p-12 text-center hover:border-primary transition-colors cursor-pointer"
                                        onClick={() => document.getElementById('file-input').click()}
                                    >
                                        <div className="text-6xl mb-4">📁</div>
                                        <h3 className="font-semibold text-xl text-neutral-dark mb-2">
                                            Drop your image here
                                        </h3>
                                        <p className="text-neutral mb-4">
                                            or click to browse
                                        </p>
                                        <p className="text-sm text-neutral-light">
                                            Supports: JPG, PNG (Max 10MB)
                                        </p>
                                        <input
                                            id="file-input"
                                            type="file"
                                            accept="image/*"
                                            onChange={handleFileSelect}
                                            className="hidden"
                                        />
                                    </div>

                                    {/* Camera Button */}
                                    <div className="mt-4 text-center">
                                        <button
                                            onClick={startCamera}
                                            className="btn-secondary"
                                        >
                                            📷 Use Camera
                                        </button>
                                    </div>
                                </>
                            )}

                            {/* Camera View */}
                            {uploadMethod === 'camera' && !preview && (
                                <div className="space-y-4">
                                    <div className="relative bg-black rounded-card overflow-hidden">
                                        <video
                                            ref={videoRef}
                                            autoPlay
                                            playsInline
                                            muted
                                            className="w-full h-auto"
                                            style={{ minHeight: '300px' }}
                                        />
                                    </div>
                                    <div className="flex gap-3">
                                        <button
                                            onClick={capturePhoto}
                                            className="btn-primary flex-1"
                                        >
                                            📸 Capture Photo
                                        </button>
                                        <button
                                            onClick={stopCamera}
                                            className="btn-secondary"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            )}

                            {/* Preview */}
                            {preview && (
                                <div>
                                    <div className="relative mb-6">
                                        <img
                                            src={preview}
                                            alt="Preview"
                                            className="w-full h-64 object-cover rounded-card"
                                        />
                                        <button
                                            onClick={resetUpload}
                                            className="absolute top-3 right-3 bg-white/90 hover:bg-white p-2 rounded-full transition-colors"
                                        >
                                            <span className="text-xl">❌</span>
                                        </button>
                                    </div>

                                    {/* Submit Button */}
                                    <button
                                        onClick={mode === 'ocr' ? handleOCRSubmit : handleSubmit}
                                        disabled={loading}
                                        className="btn-primary w-full"
                                    >
                                        {loading ? (
                                            <span className="flex items-center justify-center gap-2">
                                                <span className="animate-spin">⏳</span>
                                                {mode === 'ocr' ? 'Extracting Text...' : 'Recognizing...'}
                                            </span>
                                        ) : (
                                            mode === 'ocr' ? '📦 Extract Ingredients' : '🔍 Recognize Ingredients'
                                        )}
                                    </button>
                                </div>
                            )}
                        </>
                    )}

                    {/* Error Message */}
                    {error && (
                        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
                            {error}
                        </div>
                    )}
                </div>

                {/* Tips */}
                {mode !== 'manual' && (
                    <div className="mt-8 grid md:grid-cols-3 gap-4">
                        <div className="bg-white p-4 rounded-lg">
                            <div className="text-2xl mb-2">💡</div>
                            <p className="text-sm text-neutral">
                                Use good lighting for better results
                            </p>
                        </div>
                        <div className="bg-white p-4 rounded-lg">
                            <div className="text-2xl mb-2">📐</div>
                            <p className="text-sm text-neutral">
                                Keep ingredients clearly visible
                            </p>
                        </div>
                        <div className="bg-white p-4 rounded-lg">
                            <div className="text-2xl mb-2">🎯</div>
                            <p className="text-sm text-neutral">
                                One ingredient at a time works best
                            </p>
                        </div>
                    </div>
                )}
            </div>

            {/* Hidden canvas for camera capture */}
            <canvas ref={canvasRef} style={{ display: 'none' }} />
        </div>
    );
}
