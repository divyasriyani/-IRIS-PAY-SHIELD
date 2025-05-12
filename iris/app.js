import { useState } from "react";
import axios from "axios";

export default function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async () => {
    if (!image) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("image", image);
    
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", formData);
      setResult(response.data.prediction);
    } catch (error) {
      console.error("Error uploading image:", error);
      setResult("Error processing image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Iris Recognition</h1>
      <input type="file" accept="image/*" onChange={handleImageChange} className="mb-4" />
      {preview && <img src={preview} alt="Preview" className="w-40 h-40 object-cover mb-4 rounded-lg shadow" />}
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-600"
        disabled={loading}
      >
        {loading ? "Processing..." : "Upload & Predict"}
      </button>
      {result && <p className="mt-4 text-lg font-semibold">Prediction: {result}</p>}
    </div>
  );
}
