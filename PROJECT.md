# Fabled Fusion - PROJECT.md

## Purpose

Fabled Fusion is an experimental AI-powered Pokemon clone that demonstrates the capabilities of integrating Large Language Models and image generation AI into an interactive web game. Each monster encountered is procedurally unique in its type, appearance, and characteristics. The game serves as an exploration of how AI can power dynamic content generation in gaming, with the ultimate goal of creating a platform for users to learn and interact with AI through visual storytelling and gameplay.

## Architecture

The application follows a modern full-stack architecture with a clear separation between frontend and backend:

```
├── frontend/monster_frontend/    # Next.js 13 TypeScript frontend
│   ├── app/                      # App Router pages
│   ├── redux/                    # State management
│   └── public/                   # Static assets
│
├── monster_project/              # Django backend
│   ├── monster_app/              # Core monster management
│   ├── locations/                # Location-based gameplay
│   ├── explore/                  # Adventure generation
│   ├── battle/                   # Combat system
│   └── users/                    # User management
│
└── world_generator.py            # Procedural world generation
```

### Communication Flow
1. Frontend (Next.js) makes API requests to Django REST backend
2. Backend processes requests and communicates with OpenAI APIs (ChatGPT & DALL-E)
3. AI-generated content (images, stories) is stored and served through Django
4. Redux manages frontend state and caches API responses

## Technical Stack

### Backend
- **Framework**: Django 4.x with Django REST Framework
- **Database**: TinyDB (lightweight JSON-based database)
- **AI Integration**:
  - OpenAI ChatGPT API for adventure and story generation
  - OpenAI DALL-E API for unique monster image generation
- **Key Libraries**:
  - `django-cors-headers` - Cross-origin resource sharing
  - `django4-background-tasks` - Asynchronous task processing
  - `django-environ` - Environment variable management
  - `Pillow` - Image processing
  - `requests` - HTTP library for API calls

### Frontend
- **Framework**: Next.js 13.4.4 with App Router
- **Language**: TypeScript 5.1.3
- **UI Libraries**:
  - React 18.2.0
  - Chakra UI 2.7.0 - Component library
  - Tailwind CSS 3.3.2 - Utility-first CSS
  - Framer Motion 10.12.16 - Animations
- **State Management**: Redux Toolkit with RTK Query
- **Styling**: Emotion (CSS-in-JS) + Tailwind CSS

## Major Components

### 1. Monster Generation System (`monster_app/monster_creation/`)
The core of the game's uniqueness lies in its procedural monster generation:

- **Template-Based Creation**: Uses JSON templates for:
  - `elements.json` - Elemental types (fire, water, earth, etc.)
  - `animals.json` - Base creature types
  - `emotions.json` - Personality traits
  - `actions.json` - Behavior characteristics

- **AI Image Generation**:
  - Combines element + creature attributes into DALL-E prompts
  - Generates unique images for each monster encounter
  - Images are stored and served via Django static files

- **Monster Stats**: Each monster has:
  - Health, Attack, and XP attributes
  - Time-based recovery system (unconscious monsters heal over time)
  - Location tracking (x, y coordinates)
  - IP-based encounter tracking

### 2. Location-Based Gameplay (`locations/`)
Physical world integration through QR codes:

- **QR Code Generation**: Creates location-specific QR codes stored in `locationqrcodes/`
- **Location Database**: Tracks locations in `location_db.json`
- **Encounter System**: Different monsters appear at different physical locations
- **World Map**: Procedural generation using `world_generator.py` with terrain types:
  - Water (`~`)
  - Land (`.`)
  - Trees (`T`)
  - Mountains (`^`)

### 3. Adventure Generation (`explore/adventure_generator.py`)
Dynamic storytelling powered by ChatGPT:

- Uses story archetypes from `story_archetypes.json`
- Generates contextual adventures based on:
  - Player's current monsters
  - Location context
  - Previous adventure history
- Creates narrative-driven gameplay experiences

### 4. Battle System (`battle/`)
Turn-based combat mechanics:

- Game entity inheritance model (base stats and behavior)
- Real-time health tracking
- Battle history and timestamps
- Recovery mechanics based on time elapsed since last battle

### 5. User System (`users/`)
Player management and authentication:

- Django authentication integration
- Monster ownership tracking
- User progress persistence

### 6. Frontend Pages (`frontend/app/`)
- **Home Page** (`page.tsx`): Gallery of all discovered monsters
- **Landscape View** (`landscape/`): World map visualization
- **Monster Detail** (`monsters/`): Individual monster information
- Redux API integration with RTK Query for efficient data fetching

## Unique Features

### 1. **Truly Unique Monsters**
Unlike traditional Pokemon games with fixed species, every monster in Fabled Fusion is generated uniquely by combining:
- Element types (16,000+ variations in `elements.json`)
- Creature bases (8,000+ variations in `animals.json`)
- Personality traits and emotions
- DALL-E generated images ensuring visual uniqueness

### 2. **AI-Powered Storytelling**
The game doesn't use pre-written dialogue or quests. Instead:
- ChatGPT generates contextual adventures on-the-fly
- Stories adapt to player choices and monster collection
- Narrative emerges from gameplay rather than fixed scripts

### 3. **Physical World Integration**
QR code system bridges digital and physical gameplay:
- Real-world locations correspond to in-game locations
- Different areas spawn different monster types
- Encourages exploration of physical spaces

### 4. **Time-Based Recovery Mechanics**
Adds strategy beyond simple health potions:
- Knocked-out monsters recover based on real-world time elapsed
- Full recovery at a rate of max health per 24 hours
- Encourages monster rotation and strategic team building

### 5. **Procedural World Generation**
ASCII-based world map generation creates varied landscapes:
- Randomized terrain with islands, mountains, and forests
- Dynamic blob generation for organic shapes
- Exportable and shareable world seeds

### 6. **Educational AI Platform Potential**
Beyond gaming, the architecture demonstrates:
- How to integrate LLMs into interactive applications
- Template-based prompt engineering
- Managing AI-generated content at scale
- Creating a "visual programming language for AI"

## Development Philosophy

This project was built as an experiment using ChatGPT to assist in development, demonstrating:

- **Rapid Iteration**: Fast prototyping through AI-assisted coding
- **Full-Stack AI Integration**: Practical implementation of multiple AI APIs
- **Learning Platform**: Foundation for teaching users how to leverage AI tools

## Future Vision

The long-term goal extends beyond a simple game:

1. **AI Templating Platform**: Allow users to create their own AI-powered experiences
2. **Expanded Use Cases**: Templates for web apps, stories, and other creative projects
3. **Visual AI Programming**: Interface for non-technical users to harness AI capabilities
4. **Community-Driven Content**: User-created templates and shared experiences

## Running the Application

### Backend
```bash
cd monster_project
python manage.py runserver
```

### Frontend
```bash
cd frontend/monster_frontend
npm run dev
```

The frontend runs on `http://localhost:3000` and communicates with the Django backend on `http://127.0.0.1:8000`.
