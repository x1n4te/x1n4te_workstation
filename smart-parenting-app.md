## Tech Stack — Smart Parenting App

### Frontend (Mobile)
| Component     | Choice                                      |
| ------------- | ------------------------------------------- |
| Framework     | **React Native + Expo SDK 52**              |
| Navigation    | **Expo Router v4**                          |
| UI Library    | **React Native Paper v5**                   |
| Charts        | **react-native-chart-kit + victory-native** |
| Forms         | **React Hook Form + Zod**                   |
| State         | **Zustand**                                 |
| Storage       | **AsyncStorage + Expo SecureStore**         |
| Notifications | **Expo Notifications**                      |

### Backend
| Component    | Choice                    |
| ------------ | ------------------------- |
| Framework    | **FastAPI**               |
| Auth         | **Firebase Auth**         |
| Database     | **Supabase (PostgreSQL)** |
| ORM          | **SQLAlchemy**            |
| Task Queue   | **Celery + Redis**        |
| AI           | **OpenRouter API**        |
| File Storage | **Supabase Storage**      |

### AI Engine
| Component         | Choice                                         |
| ----------------- | ---------------------------------------------- |
| Model             | **Qwen2.5-3B (via OpenRouter) or GPT-4o-mini** |
| Framework         | **Instructor**                                 |
| Pattern Detection | **Pandas + NumPy**                             |
| Prompt Templates  | **Jinja2**                                     |

### DevOps
| Component       | Choice                                                   |
| --------------- | -------------------------------------------------------- |
| Backend Hosting | **Supabase** (for DB) + **Railway/Fly.io** (for FastAPI) |
| Mobile Build    | **Expo EAS Build**                                       |
| CI/CD           | **GitHub Actions**                                       |
| Monitoring      | **Sentry**                                               |

---

## Database Schema
```sql
-- Users (parents)
users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  name TEXT,
  created_at TIMESTAMP
)

-- Child profiles
children (
  id UUID PRIMARY KEY,
  parent_id UUID REFERENCES users(id),
  name TEXT,
  date_of_birth DATE,
  created_at TIMESTAMP
)

-- Activity logs
activities (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES children(id),
  type TEXT,  -- screen_time, sleep, meal, education
  value JSONB,  -- flexible: {minutes: 120} or {meal_type: "breakfast", quality: "good"}
  recorded_at TIMESTAMP,
  created_at TIMESTAMP
)

-- AI recommendations
recommendations (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES children(id),
  content TEXT,  -- AI-generated recommendation
  category TEXT,  -- screen_time, sleep, nutrition, education
  priority TEXT,  -- low, medium, high
  based_on JSONB,  -- the activity data that triggered this
  created_at TIMESTAMP
)

-- Alerts
alerts (
  id UUID PRIMARY KEY,
  child_id UUID REFERENCES children(id),
  type TEXT,  -- excessive_screen_time, irregular_sleep, missed_meal
  message TEXT,
  severity TEXT,  -- info, warning, critical
  acknowledged BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP
)

-- Admin
admins (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  role TEXT  -- admin, moderator
)
```

---

## AI Prompt Template
```python
ACTIVITY_ANALYSIS_PROMPT = """
You are a child development advisor analyzing activity data for a {age}-year-old child.

Activity Summary (last 7 days):
{activity_data_json}

Analyze this data and provide:
1. **Patterns detected** — recurring behaviors or trends
2. **Concerns** — irregularities or unhealthy patterns
3. **Recommendations** — 3-5 specific, actionable suggestions for parents
4. **Positive observations** — what the child is doing well

Respond in JSON:
{
  "patterns": [{"type": "...", "description": "...", "confidence": 0.0-1.0}],
  "concerns": [{"type": "...", "description": "...", "severity": "low/medium/high"}],
  "recommendations": [{"category": "...", "suggestion": "...", "priority": "low/medium/high"}],
  "positives": ["..."]
}

Use plain language. No medical advice. Focus on routine and habits.
"""
```

---

## API Endpoints
```
POST   /api/auth/signup              -- parent registration
POST   /api/auth/login               -- parent login
POST   /api/auth/logout              -- session end

GET    /api/children                 -- list children
POST   /api/children                 -- create child profile
GET    /api/children/:id             -- child detail
PUT    /api/children/:id             -- update child
DELETE /api/children/:id             -- delete child

POST   /api/activities               -- log activity
GET    /api/activities/:child_id     -- get activity history
GET    /api/activities/:child_id/summary -- aggregated stats

POST   /api/ai/analyze/:child_id     -- trigger AI analysis
GET    /api/ai/recommendations/:child_id -- get recommendations
GET    /api/ai/patterns/:child_id    -- get detected patterns

GET    /api/alerts/:child_id         -- get alerts
PUT    /api/alerts/:id/acknowledge   -- mark alert as read

GET    /api/admin/users              -- list users (admin only)
GET    /api/admin/stats              -- system stats (admin only)
```

---

## Mobile App Screens (12 total)
```
1.  Login screen
2.  Signup screen
3.  Home dashboard (child cards + summary)
4.  Child profile creation
5.  Child profile edit
6.  Activity logging — screen time
7.  Activity logging — sleep
8.  Activity logging — meals
9.  Activity logging — education
10. Activity history / logs view
11. AI recommendations page
12. AI pattern analysis page
13. Visual reports / charts
14. Alerts / notifications list
15. Profile / settings
16. Admin panel (user management)
```

---

## Cost Estimate of Components

| Component                  | Monthly Cost                                                                  |
| -------------------------- | ----------------------------------------------------------------------------- |
| Supabase (free tier)       | $0                                                                            |
| Firebase Auth (free tier)  | $0                                                                            |
| OpenRouter / AI API        | ~$5-10 (depends on usage, but pwede rin free tiers or locally hosted ung llm) |
| Railway/Fly.io (backend)   | $5-10 (if need ng deployed version and not localhost lang.)                   |
| Expo EAS Build (free tier) | $0                                                                            |
| **Total**                  | **~$10-20/month = PHP 600-1200**                                              |

---

## Project Structure
```
smart-parenting-app/
├── mobile/                    # React Native + Expo
│   ├── app/                   # Expo Router pages
│   │   ├── (auth)/            # Login, Signup
│   │   ├── (tabs)/            # Dashboard, AI, Reports, Profile
│   │   └── admin/             # Admin panel
│   ├── components/            # Reusable UI components
│   ├── hooks/                 # Custom hooks (useAuth, useActivities)
│   ├── lib/                   # API client, utils
│   ├── stores/                # Zustand state stores
│   └── app.json               # Expo config
├── backend/                   # FastAPI
│   ├── api/routes/            # API endpoints
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   │   ├── ai_service.py      # AI analysis engine
│   │   ├── activity_service.py # Activity processing
│   │   └── alert_service.py   # Alert generation
│   ├── prompts/               # AI prompt templates
│   └── main.py                # FastAPI entry
├── docs/                      # Documentation
└── README.md
```
