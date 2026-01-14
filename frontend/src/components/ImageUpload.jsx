import React, { useState } from 'react';

const ImageUpload = ({ onUpload, onRecognize }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setError('');

        if (file) {
            // Validate file type
            const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
            if (!validTypes.includes(file.type)) {
                setError('Please select a valid image file (JPG, JPEG, or PNG)');
                setSelectedFile(null);
                setPreview(null);
                return;
            }

            // Validate file size (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                setError('File size must be less than 5MB');
                setSelectedFile(null);
                setPreview(null);
                return;
            }

            setSelectedFile(file);

            // Create preview
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleUpload = () => {
        if (selectedFile && onUpload) {
            onUpload(selectedFile);
        }
    };

    const handleRecognize = () => {
        if (selectedFile && onRecognize) {
            onRecognize(selectedFile);
        }
    };

    return (
        <div className="card">
            <h3>Upload Ingredient Image</h3>

            <input
                type="file"
                accept="image/jpeg,image/jpg,image/png"
                onChange={handleFileChange}
            />

            {error && <div className="error">{error}</div>}

            {preview && (
                <div style={{ marginTop: '20px' }}>
                    <img
                        src={preview}
                        alt="Preview"
                        style={{
                            maxWidth: '100%',
                            maxHeight: '400px',
                            borderRadius: '8px',
                            display: 'block',
                            margin: '0 auto'
                        }}
                    />
                </div>
            )}

            {selectedFile && (
                <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
                    <button onClick={handleRecognize} className="btn btn-primary">
                        Recognize Ingredients
                    </button>
                    <button onClick={handleUpload} className="btn btn-secondary">
                        Upload Only
                    </button>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
