import { useNavigate } from "react-router-dom";

const Index = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen flex items-center justify-center gap-10">
            <button
                onClick={() => navigate("/mango")}
                className="px-8 py-6 bg-green-600 text-white rounded-xl text-lg"
            >
                Mango Detection
            </button>

            <button
                onClick={() => navigate("/cashew")}
                className="px-8 py-6 bg-orange-600 text-white rounded-xl text-lg"
            >
                Cashew Detection
            </button>
        </div>
    );
};

export default Index;
