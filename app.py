# Force Trigger
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SAHU JI Athletics | Performance Sportswear</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
            body { font-family: 'Inter', sans-serif; }
        </style>
    </head>
    <body class="bg-black text-white">
        <nav class="p-6 flex justify-between items-center border-b border-gray-800">
            <h1 class="text-2xl font-black tracking-tighter">SAHU JI</h1>
            <div class="space-x-6 text-sm font-medium uppercase tracking-widest text-gray-400">
                <a href="#" class="hover:text-white transition">Training</a>
                <a href="#" class="hover:text-white transition">Lifestyle</a>
                <a href="#" class="hover:text-white transition">E-Sports</a>
            </div>
        </nav>

        <header class="relative h-[80vh] flex items-center justify-center overflow-hidden">
            <div class="z-10 text-center px-4">
                <h2 class="text-6xl md:text-8xl font-black italic uppercase tracking-tighter mb-4">
                    Limitless <span class="text-blue-600">Motion</span>
                </h2>
                <p class="max-w-xl mx-auto text-gray-400 text-lg mb-8">
                    Engineered for high-intensity performance. From the pitch to the server, stay ahead of the game.
                </p>
                <div class="flex gap-4 justify-center">
                    <button class="bg-white text-black px-8 py-4 font-bold uppercase hover:bg-gray-200 transition">Shop Training</button>
                    <button class="border border-white px-8 py-4 font-bold uppercase hover:bg-white hover:text-black transition">Explore Gear</button>
                </div>
            </div>
            <div class="absolute inset-0 opacity-20 pointer-events-none">
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500 rounded-full blur-[120px]"></div>
            </div>
        </header>

        <section class="grid grid-cols-1 md:grid-cols-3 gap-1 border-t border-gray-800 bg-gray-800">
            <div class="bg-black p-12 text-center">
                <h3 class="text-4xl font-black mb-2">3.5Y+</h3>
                <p class="text-gray-500 uppercase text-xs tracking-widest">Innovation Heritage</p>
            </div>
            <div class="bg-black p-12 text-center border-l border-r border-gray-800">
                <h3 class="text-4xl font-black mb-2">PRO-DRY</h3>
                <p class="text-gray-500 uppercase text-xs tracking-widest">Moisture Tech</p>
            </div>
            <div class="bg-black p-12 text-center">
                <h3 class="text-4xl font-black mb-2">GLOBAL</h3>
                <p class="text-gray-500 uppercase text-xs tracking-widest">Standard Shipping</p>
            </div>
        </section>

        <footer class="p-10 text-center text-gray-600 text-sm">
            &copy; 2026 SAHU JI Athletics. Deployment via GitHub Actions Complete.
        </footer>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Keep port 5000 to match your AWS Inbound Rules
    app.run(host='0.0.0.0', port=5000)