# Canteen AI - Product Requirements Document

**Document Version**: 1.0
**Last Updated**: 2026-08-10
**Status**: In Development (Phase 1-2)

---

## 📋 Table of Contents

1. [Product Overview](#product-overview)
2. [Target Users & Roles](#target-users--roles)
3. [Vision & Goals](#vision--goals)
4. [Core Functional Requirements](#core-functional-requirements)
5. [Feature Priority Matrix](#feature-priority-matrix)
6. [Non-Functional Requirements](#non-functional-requirements)
7. [AI Feature Requirements](#ai-feature-requirements)
8. [Security Requirements](#security-requirements)
9. [Database Architecture](#database-architecture)
10. [API Architecture](#api-architecture)
11. [Frontend Architecture](#frontend-architecture)
12. [Out-of-Scope Items](#out-of-scope-items)
13. [Future Scope](#future-scope)

---

## 🎯 Product Overview

**Canteen AI** is an AI-powered student food, budget, and habit tracker that helps students:

- **Track spending** on canteen/food purchases
- **Manage budgets** with daily, weekly, and monthly limits
- **Monitor eating habits** and food consumption patterns
- **Scan food images** using AI vision to identify meals and estimate nutrition
- **Analyze trends** in spending and food choices over time
- **Receive personalized insights** and health recommendations
- **Make informed decisions** about food purchases and dietary habits

### Key Value Propositions

1. **Budget Control**: Empower students to spend responsibly
2. **Health Awareness**: Help students understand their eating patterns
3. **Data-Driven Insights**: Leverage AI to provide actionable recommendations
4. **Simple & Intuitive**: Easy-to-use interface for students
5. **Admin Efficiency**: Help canteen operators manage inventory and analytics

---

## 👥 Target Users & Roles

### Primary Users

1. **Students** (User Role)
   - College/university students aged 18-25
   - Budget-conscious, nutrition-aware
   - Regular canteen users
   - Access on mobile and desktop

2. **Canteen Administrators** (Admin Role)
   - Canteen/food court staff
   - Inventory managers
   - Analytics viewers
   - Food pricing managers

### User Roles & Permissions

| Feature | Student | Admin |
|---------|---------|-------|
| Browse Food Items | ✅ | ✅ |
| Make Purchases | ✅ | ❌ |
| Scan Food Images | ✅ | ❌ |
| View Own Analytics | ✅ | ❌ |
| Manage Budget | ✅ | ❌ |
| Add Food Items | ❌ | ✅ |
| Edit Food Items | ❌ | ✅ |
| Manage Prices | ❌ | ✅ |
| View All Analytics | ❌ | ✅ |
| User Management | ❌ | ✅ |

---

## 🚀 Vision & Goals

### Mission Statement

Empower students to make informed financial and dietary decisions through real-time budget tracking and AI-powered food analysis.

### Strategic Goals

1. **Financial Literacy**: Help students track and control spending
2. **Health Awareness**: Increase awareness of eating patterns and nutrition
3. **Behavior Change**: Encourage healthier food choices through insights
4. **Operational Efficiency**: Provide canteens with actionable business intelligence
5. **Scalability**: Design for deployment across multiple institutions

### Success Metrics

- **User Adoption**: 70%+ of student body within 6 months
- **Budget Compliance**: 80%+ of users stay within budget alerts
- **Engagement**: 50%+ weekly active users
- **Data Quality**: 95%+ accurate AI food recognition
- **Performance**: <500ms response time for all endpoints

---

## 📊 Core Functional Requirements

### 1. AUTHENTICATION & AUTHORIZATION

#### Registration
- [ ] User registration endpoint
- [ ] Password strength validation
- [ ] Email verification (future)
- [ ] OAuth integration (future)

#### Login & Session Management
- [ ] JWT-based authentication
- [ ] Secure password hashing (bcrypt/argon2)
- [ ] Session expiry and refresh tokens
- [ ] Login history
- [ ] Device tracking (future)

#### Authorization & Roles
- [ ] Role-based access control (RBAC)
- [ ] Admin role with elevated permissions
- [ ] Student role with standard permissions
- [ ] Permission enforcement on all endpoints
- [ ] API key authentication for integrations (future)

#### Account Management
- [ ] Change password
- [ ] Reset password via email
- [ ] Update profile information
- [ ] View account settings
- [ ] Delete account (GDPR compliance)

---

### 2. BUDGET MANAGEMENT

#### Budget Setup & Configuration
- [x] Set monthly budget limit
- [ ] Set weekly budget limit
- [ ] Set daily budget limit
- [ ] Multiple budget periods support
- [ ] Budget reset scheduling

#### Budget Monitoring
- [x] Current spending display
- [x] Remaining budget calculation
- [x] Budget utilization percentage
- [x] Budget status (Within/At/Over)
- [ ] Real-time budget updates

#### Budget Alerts & Notifications
- [ ] Alert when reaching 75% of budget
- [ ] Alert when reaching 100% of budget
- [ ] Alert when exceeding budget
- [ ] Customizable alert thresholds
- [ ] Alert frequency settings

#### Budget History & Analytics
- [ ] Budget change history
- [ ] Historical budget comparison
- [ ] Trend analysis over multiple months
- [ ] Budget vs actual spending chart
- [ ] Export budget reports

---

### 3. FOOD & PURCHASE TRACKING

#### Food Catalogue Management
- [x] Browse all available food items
- [x] Food item details (name, category, price, nutrition)
- [ ] Food availability status
- [ ] Food item images
- [ ] Allergen information
- [ ] Dietary preferences tags (vegan, vegetarian, etc.)

#### Purchase Recording
- [x] Add purchase (select food + quantity)
- [ ] Edit existing purchase
- [ ] Delete purchase
- [ ] Bulk purchase (multiple items in one transaction)
- [ ] Receipt parsing (future)

#### Purchase History
- [x] View all purchases
- [ ] Filter purchases by date range
- [ ] Filter purchases by food category
- [ ] Search purchases
- [ ] Sort by date, price, category
- [ ] Purchase export/download

#### Transaction Recording
- [x] Record purchase date/time
- [x] Record quantity
- [x] Record amount paid
- [ ] Payment method tracking
- [ ] Receipt image attachment

---

### 4. FOOD HABIT TRACKING

#### Habit Analytics
- [x] Meals logged count
- [x] Food categories breakdown
- [x] Frequently purchased foods (top 5)
- [x] Purchase frequency by food
- [ ] Meal timing patterns (breakfast, lunch, dinner)
- [ ] Time-of-day eating patterns

#### Nutritional Tracking
- [x] Daily calorie summary
- [x] Protein intake tracking
- [x] Carbohydrate tracking
- [x] Fat intake tracking
- [x] Sugar intake tracking
- [ ] Fiber tracking (when available)
- [ ] Micronutrient tracking (future)

#### Health Scoring
- [x] Healthy eating score calculation
- [x] Score-based recommendations
- [x] Category-based health classification
- [ ] Personalized wellness goals
- [ ] Dietary restriction support

#### Trend Analysis
- [x] Weekly spending comparison
- [x] Monthly spending comparison
- [ ] Seasonal pattern detection
- [ ] Year-over-year analysis
- [ ] Predictive spending trends

---

### 5. AI FOOD IMAGE SCANNER

#### Image Capture & Upload
- [ ] Take photo directly from app
- [ ] Upload photo from gallery
- [ ] Drag-and-drop upload
- [ ] Webcam capture support
- [ ] Image file type validation
- [ ] Image size optimization (max 5MB)
- [ ] Batch upload support (future)

#### AI Food Recognition
- [ ] Send image to vision API service
- [ ] Identify visible food items
- [ ] Detect multiple items in image
- [ ] Confidence score for each detection
- [ ] Return detected food names

#### Nutrition Estimation
- [ ] Estimate serving/portion size from image
- [ ] Estimate calories
- [ ] Estimate protein
- [ ] Estimate carbohydrates
- [ ] Estimate fat
- [ ] Estimate fiber (when possible)
- [ ] Estimate sodium (when possible)

#### Meal Categorization
- [ ] Identify meal type (breakfast, lunch, dinner, snack)
- [ ] Detect meal components
- [ ] Dietary classification (vegan, vegetarian, etc.)
- [ ] Healthy/unhealthy classification

#### User Review & Correction
- [ ] Display AI-detected items clearly
- [ ] Show all nutrition estimates
- [ ] Allow user to edit detected items
- [ ] Allow user to remove incorrect detections
- [ ] Allow user to add missing items
- [ ] Allow user to override nutrition values
- [ ] Confirm analysis before saving
- [ ] Show estimate disclaimers

#### Save & Link
- [ ] Save confirmed food scan to history
- [ ] Link scan to purchase record (optional)
- [ ] Create custom food item from scan
- [ ] Add to favorites
- [ ] Scan history view

---

### 6. AI INSIGHTS & ANALYTICS

#### Spending Analytics
- [x] Monthly spending summary
- [x] Category spending breakdown
- [x] Average daily spending
- [ ] Weekly spending trends
- [ ] Spending by day of week
- [ ] Spending by time of day
- [ ] Most expensive items

#### Food Habit Insights
- [ ] Most frequently purchased foods
- [ ] Food preference patterns
- [ ] Healthiest purchases
- [ ] Least healthy purchases
- [ ] Dietary balance assessment
- [ ] Eating time patterns

#### Predictive Analytics
- [ ] Predict next month spending (if sufficient data)
- [ ] Forecast budget overspend risk
- [ ] Suggest budget adjustments
- [ ] Identify outlier spending days
- [ ] Recommend spending reduction opportunities

#### AI-Generated Recommendations
- [ ] Personalized spending insights ("You spent 20% more on snacks this week")
- [ ] Health recommendations ("Try adding more fruits to your diet")
- [ ] Budget-related suggestions ("Reduce coffee purchases to save ₹500/month")
- [ ] Alternative food recommendations ("Consider X instead of Y for better nutrition")
- [ ] Wellness tips based on eating patterns

#### Insight Presentation
- [ ] Clear, non-technical explanations
- [ ] Data visualization (charts, graphs)
- [ ] Actionable insights only
- [ ] Confidence/uncertainty indicators
- [ ] Source data attribution

---

### 7. GOALS & PERSONAL TARGETS

#### Goal Creation
- [ ] Create spending goals (e.g., "Limit to ₹2000/month")
- [ ] Create health goals (e.g., "Increase healthy meals to 60%")
- [ ] Create nutrition goals (e.g., "Reduce sugar intake")
- [ ] Set goal duration (weekly, monthly, custom)
- [ ] Set goal target values

#### Goal Tracking
- [ ] Progress visualization (progress bar, chart)
- [ ] Current vs target display
- [ ] Goal status (On Track, At Risk, Exceeded)
- [ ] Days remaining in goal period
- [ ] Achievement notifications

#### Goal History
- [ ] Completed goals list
- [ ] Goal performance statistics
- [ ] Streak tracking (e.g., "7-day healthy eating streak")
- [ ] Goal reset/renewal
- [ ] Goal achievement badges (future)

---

### 8. NOTIFICATIONS & ALERTS

#### In-App Notifications
- [ ] Budget alerts (75%, 100%, exceeded)
- [ ] Goal status updates
- [ ] Weekly spending summary
- [ ] Important AI insights
- [ ] New food items available
- [ ] Special offers/promotions (future)

#### Notification Center
- [ ] Notification history
- [ ] Mark as read/unread
- [ ] Filter by type
- [ ] Notification settings (enable/disable)
- [ ] Notification preferences

#### Email Notifications (Future)
- [ ] Weekly digest email
- [ ] Alert emails for budget events
- [ ] Personalized recommendation emails

---

### 9. DASHBOARD & HOME SCREEN

#### Student Dashboard
- [x] Current budget overview
- [x] Remaining budget display
- [x] Budget utilization percentage
- [x] Budget status indicator
- [ ] Quick spending summary (Today/Week/Month)
- [x] Recent purchases list
- [ ] Recent food scans
- [ ] Quick "Scan Food" action button
- [x] Health score card
- [ ] Top insights widget
- [ ] Goals progress widget
- [ ] Spending trend chart
- [ ] Category breakdown chart

#### Admin Dashboard
- [ ] Total sales overview
- [ ] Popular food items
- [ ] Category sales breakdown
- [ ] Revenue trends
- [ ] User activity metrics
- [ ] Food item availability status
- [ ] Inventory levels (future)
- [ ] Peak hours analysis
- [ ] Quick actions (add food, edit price)

---

### 10. ADMIN FEATURES

#### Food Item Management
- [ ] Add new food items
- [ ] Edit food item details
- [ ] Delete/deactivate food items
- [ ] Bulk import food items
- [ ] Set/update prices
- [ ] Manage food categories
- [ ] Set availability status
- [ ] Add food images

#### Category Management
- [ ] Create food categories
- [ ] Edit category details
- [ ] Delete categories
- [ ] Category usage statistics

#### Price Management
- [ ] Set base price
- [ ] Schedule price changes
- [ ] Apply discounts
- [ ] View price history
- [ ] Price comparison reports

#### Analytics & Reporting
- [ ] Sales by food item
- [ ] Revenue trends
- [ ] Popular items report
- [ ] Spending patterns report
- [ ] Student activity metrics
- [ ] Export reports (CSV, PDF)

#### User Management
- [ ] View all users
- [ ] User details
- [ ] Block/suspend user
- [ ] View user analytics
- [ ] Send announcements (future)

---

## 📈 Feature Priority Matrix

### PHASE 1 - Foundation (Weeks 1-2)
**Status**: In Progress

- [x] Database setup & schema
- [x] User & Food Item models
- [x] Basic CRUD operations
- [x] Purchase tracking (basic)
- [x] Budget management (basic)
- [x] Sample dashboard
- [x] Seed data
- [ ] .env configuration
- [ ] Error handling
- [ ] Input validation

### PHASE 2 - Authentication & Authorization (Weeks 3-4)

- [ ] JWT authentication
- [ ] Password hashing
- [ ] User registration endpoint
- [ ] Login endpoint
- [ ] Protected routes
- [ ] Role-based authorization
- [ ] Admin authentication
- [ ] Logout functionality

### PHASE 3 - Enhanced Purchase & Budget (Weeks 5-6)

- [ ] Edit/Delete purchases
- [ ] Edit/Delete food items
- [ ] Purchase filtering & search
- [ ] Budget alerts
- [ ] Weekly/daily budgets
- [ ] Budget history
- [ ] Input validation
- [ ] Error responses

### PHASE 4 - Food Tracking & Analytics (Weeks 7-8)

- [ ] Enhanced analytics
- [ ] Nutrition tracking
- [ ] Food habit analysis
- [ ] Spending predictions
- [ ] Trend analysis
- [ ] Export functionality
- [ ] Advanced filtering

### PHASE 5 - AI Food Scanner (Weeks 9-12)

- [ ] Image upload functionality
- [ ] Vision API integration
- [ ] Food recognition
- [ ] Nutrition estimation
- [ ] User review interface
- [ ] Save food scans
- [ ] Scan history

### PHASE 6 - AI Insights (Weeks 13-14)

- [ ] AI insight generation
- [ ] Personalized recommendations
- [ ] Spending analysis
- [ ] Habit insights
- [ ] Predictive analytics

### PHASE 7 - Goals & Notifications (Weeks 15-16)

- [ ] Goal creation & tracking
- [ ] Notification system
- [ ] In-app notifications
- [ ] Budget alerts
- [ ] Weekly summaries

### PHASE 8 - Admin Dashboard (Weeks 17-18)

- [ ] Admin authentication
- [ ] Admin dashboard
- [ ] Food management interface
- [ ] Analytics dashboard
- [ ] User management

### PHASE 9 - UI/UX Refinement (Weeks 19-20)

- [ ] Component library
- [ ] Consistent styling
- [ ] Responsive design
- [ ] Accessibility
- [ ] Mobile optimization
- [ ] Loading states
- [ ] Empty states

### PHASE 10 - Testing & Security (Weeks 21-22)

- [ ] Unit tests (backend)
- [ ] Integration tests
- [ ] API tests
- [ ] Frontend tests
- [ ] Security audit
- [ ] Input validation
- [ ] Error handling

### PHASE 11 - CI/CD & DevOps (Weeks 23-24)

- [ ] GitHub Actions setup
- [ ] Automated testing
- [ ] Linting & formatting
- [ ] Code quality checks
- [ ] Deployment pipeline

### PHASE 12 - Deployment & Docs (Weeks 25-26)

- [ ] API documentation
- [ ] Database documentation
- [ ] Architecture documentation
- [ ] Deployment guide
- [ ] User guide
- [ ] Admin guide
- [ ] Production deployment

---

## 🔒 Non-Functional Requirements

### Performance

- **API Response Time**: < 500ms for 95% of requests
- **Dashboard Load**: < 2 seconds
- **Image Upload**: < 10 seconds (with AI processing)
- **Database Query**: < 200ms for analytics queries
- **Concurrent Users**: Support 1000+ concurrent users
- **Cache**: Implement Redis for session & frequently accessed data (future)

### Scalability

- **Database**: PostgreSQL with connection pooling
- **Horizontal Scaling**: Stateless backend for load balancing
- **CDN**: Static assets via CDN for images
- **Database Sharding**: Plan for future multi-tenant support (future)

### Availability & Reliability

- **Uptime**: 99.5% availability target
- **Error Rate**: < 0.5% error rate
- **Graceful Degradation**: System functions with degraded AI features if API unavailable
- **Data Backups**: Daily automated backups

### Security (See Security Section Below)

### Usability

- **Intuitive UI**: Minimal learning curve
- **Mobile Responsive**: Works on phones, tablets, desktops
- **Accessibility**: WCAG 2.1 AA compliance
- **Internationalization**: Support for multiple languages (future)
- **Loading States**: Clear feedback during operations
- **Error Messages**: Clear, actionable error messages

### Maintainability

- **Code Quality**: Clean, well-documented code
- **Code Style**: Consistent formatting (Prettier, Black)
- **Testing**: >80% code coverage
- **Documentation**: API docs, architecture docs, database docs
- **Logging**: Structured logging for debugging

### Compatibility

- **Backend**: Python 3.9+
- **Frontend**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Database**: PostgreSQL 12+
- **API Format**: RESTful JSON API

---

## 🤖 AI Feature Requirements

### AI Vision Service Integration

#### Service Requirements
- **Provider**: Azure Computer Vision, Google Vision API, or similar
- **Capabilities**: Food object detection, multi-item recognition
- **Accuracy**: Minimum 85% accuracy for food identification
- **Latency**: < 5 seconds response time
- **Cost Model**: Evaluate per-request or subscription pricing

#### Food Recognition
- Identify single food items
- Detect multiple food items in one image
- Handle different presentations (cooked, raw, plated)
- Confidence scores for each detection
- Fallback for unrecognized foods

#### Nutrition Estimation
- Estimate portion size from image context
- Calculate calories per estimated serving
- Protein, carbs, fat, fiber estimation
- Sodium, sugar estimation where possible
- Uncertainty/confidence indicators

#### Disclaimers & Limitations
- **ALL** nutrition values must be labeled as "ESTIMATES"
- Clear disclaimer: "AI-generated estimates are not medically accurate"
- Recommendation to verify critical values
- Encourage user review and correction
- No medical claims (no "this food is healthy/unhealthy")

### AI Analytics Engine

#### Capabilities
- Historical trend analysis
- Spending pattern detection
- Food preference analysis
- Predictive spending (if sufficient data)
- Anomaly detection

#### Implementations
- Python/Pandas for data analysis
- Scikit-learn for predictive models (future)
- Time-series analysis for trends
- Statistical methods for insights

#### Insights Generation
- Personalized, actionable recommendations
- Plain language explanations
- Visual representations of insights
- Confidence levels
- Data sources referenced

#### Limitations
- No medical advice
- No diet recommendations for specific conditions
- No diagnosis capabilities
- General wellness tips only

---

## 🔐 Security Requirements

### Authentication & Authorization

- [ ] JWT tokens for API authentication
- [ ] Secure password hashing (bcrypt, Argon2, or PBKDF2)
- [ ] Password strength requirements (min 8 chars, mixed case, numbers, symbols)
- [ ] Account lockout after failed attempts (5 attempts, 15 min lockout)
- [ ] Multi-factor authentication (future)
- [ ] Session timeout (15 min inactivity)
- [ ] Refresh token rotation
- [ ] CORS properly configured

### Data Protection

- [ ] HTTPS/TLS for all communications
- [ ] Password never logged or displayed
- [ ] PII encryption at rest (future)
- [ ] Database connection encryption
- [ ] API key rotation mechanism
- [ ] Secrets management (environment variables only)
- [ ] No hardcoded credentials (fix existing issues)

### Input Validation & Sanitization

- [ ] All API inputs validated
- [ ] Email format validation
- [ ] Numeric field bounds checking
- [ ] String length limits
- [ ] SQL injection prevention (SQLAlchemy ORM)
- [ ] XSS prevention (React auto-escaping)
- [ ] File upload validation (type, size, scanning)
- [ ] Rate limiting on APIs

### Error Handling & Logging

- [ ] No internal error exposure to users
- [ ] Generic error messages to clients
- [ ] Structured server-side logging
- [ ] Error tracking (Sentry or similar - future)
- [ ] Audit logging for sensitive operations
- [ ] No sensitive data in logs

### Infrastructure Security

- [ ] Database access control (least privilege)
- [ ] Environment isolation (dev, staging, prod)
- [ ] Secrets in environment variables
- [ ] Database backups encrypted
- [ ] API rate limiting
- [ ] DDoS protection (future)
- [ ] Web Application Firewall (future)

### Compliance

- [ ] GDPR compliance (user data rights)
- [ ] Data retention policies
- [ ] User data export capability
- [ ] Right to be forgotten (account deletion)
- [ ] Privacy policy
- [ ] Terms of service
- [ ] Disclaimer about AI estimates

### File Upload Security

- [ ] File type whitelist (jpg, png, gif, webp only)
- [ ] File size limit (max 5MB)
- [ ] Filename sanitization
- [ ] Scan for malware/scripts (future)
- [ ] Store outside web root
- [ ] CDN delivery with restrictions
- [ ] Secure temporary storage

---

## 🗄️ Database Architecture

### Entities

#### User
```
- user_id (PK)
- name
- email (unique)
- password_hash
- role (student, admin)
- department
- year
- profile_picture_url
- bio
- dietary_preferences (JSON - vegetarian, vegan, allergies)
- created_at
- updated_at
- last_login
- is_active
```

#### FoodItem
```
- item_id (PK)
- name
- category_id (FK)
- description
- price
- image_url
- availability_status (available, unavailable)
- calories
- protein
- carbs
- fat
- fiber
- sugar
- sodium
- allergens (JSON array)
- dietary_tags (JSON - vegan, vegetarian, gluten-free)
- created_at
- updated_at
- created_by (FK - admin user)
```

#### FoodCategory
```
- category_id (PK)
- name
- description
- icon_url
- created_at
```

#### Purchase
```
- purchase_id (PK)
- user_id (FK)
- item_id (FK)
- quantity
- amount_paid
- purchase_time (timestamp)
- payment_method
- receipt_image_url
- created_at
```

#### Budget
```
- budget_id (PK)
- user_id (FK)
- budget_type (daily, weekly, monthly)
- limit_amount
- start_date
- end_date
- is_active
- created_at
- updated_at
```

#### FoodScan
```
- scan_id (PK)
- user_id (FK)
- image_url
- upload_time
- ai_raw_response (JSON)
- detected_items (JSON array)
- user_confirmed (boolean)
- linked_purchase_id (FK - nullable)
- created_at
```

#### FoodScanItem
```
- scan_item_id (PK)
- scan_id (FK)
- detected_food_name
- confidence_score
- portion_estimate
- calories_estimate
- protein_estimate
- carbs_estimate
- fat_estimate
- fiber_estimate
- user_corrected (boolean)
- corrected_values (JSON - if edited)
- created_at
```

#### Goal
```
- goal_id (PK)
- user_id (FK)
- goal_type (spending, health_score, nutrition)
- target_value
- current_value
- start_date
- end_date
- status (active, completed, abandoned)
- created_at
- updated_at
```

#### Notification
```
- notification_id (PK)
- user_id (FK)
- type (budget_alert, goal_update, insight, general)
- title
- message
- is_read
- action_url
- created_at
```

#### AIInsight
```
- insight_id (PK)
- user_id (FK)
- insight_type (spending, habit, health, prediction)
- title
- content
- confidence_score
- data_points (JSON)
- related_period (date range)
- created_at
- is_dismissed
```

### Schema Notes

- Foreign keys with cascade delete where appropriate
- Indexes on frequently queried columns
- Partitioning for large tables (future)
- JSON columns for flexible data (allergens, dietary tags, AI responses)

---

## 🔌 API Architecture

### Base URL
```
http://api.canteen-ai.local/api/v1
```

### Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Optional message",
  "errors": []
}
```

### Authentication
- Bearer token in Authorization header
- JWT tokens with 1-hour expiry
- Refresh tokens for extended sessions

### Rate Limiting
- 100 requests per minute per IP (unauthenticated)
- 1000 requests per minute per user (authenticated)

### Versioning
- API version in URL path (/api/v1)
- Backward compatibility maintained

### Error Codes
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 422: Unprocessable Entity
- 429: Too Many Requests
- 500: Internal Server Error

---

## 🎨 Frontend Architecture

### Technology Stack
- **Framework**: React 19.x
- **Build Tool**: Vite 8.x
- **Styling**: Tailwind CSS 4.x
- **HTTP Client**: Axios
- **Routing**: React Router 7.x
- **Charts**: Recharts 3.x
- **Icons**: Lucide React
- **State Management**: React Context (minimal) or Zustand (future)

### Project Structure
```
src/
├── components/
│   ├── common/
│   ├── auth/
│   ├── budget/
│   ├── purchases/
│   ├── scanner/
│   └── analytics/
├── pages/
│   ├── Dashboard
│   ├── Login
│   ├── Register
│   ├── Purchases
│   ├── Scanner
│   └── Profile
├── services/
│   ├── api.js
│   └── auth.js
├── hooks/
│   ├── useAuth
│   └── useFetch
├── utils/
│   ├── formatters
│   └── validators
├── layouts/
├── App.jsx
└── main.jsx
```

### Key Features
- Responsive mobile-first design
- Client-side form validation
- Loading states and error boundaries
- Lazy loading for routes
- Image optimization
- Accessibility best practices

---

## 📦 Out-of-Scope Items (for MVP)

1. **Advanced AI Features**
   - Medical diagnosis
   - Personalized diet plans
   - Drug interaction warnings
   - Condition-specific recommendations

2. **Third-Party Integrations**
   - Fitness tracker integration (Fitbit, Apple Health)
   - Payment gateway integration (initial MVP is free)
   - Email newsletter service
   - SMS notifications
   - Social sharing

3. **Advanced Features**
   - Multi-language support
   - Multi-currency support
   - Offline mode
   - Mobile app (native - web-first initially)
   - Voice commands
   - Chatbot

4. **Admin Features** (for later phases)
   - Inventory management
   - Staff management
   - Employee payroll
   - Supplier management
   - Marketing analytics

5. **Advanced Analytics** (for later phases)
   - Detailed nutritional reports
   - Health score benchmarking
   - Cohort analysis
   - Predictive models with >90% accuracy
   - Custom report builder

---

## 🔮 Future Scope (Post-MVP)

### Phase 13 - Enhanced Features
- Multi-language support
- Real payment integration
- Email notifications
- SMS alerts
- API keys for third-party developers
- Webhook support

### Phase 14 - Social Features
- Food sharing with friends
- Challenges/competitions
- Community insights
- Leaderboards
- Food ratings and reviews

### Phase 15 - Advanced Analytics
- Advanced predictive models
- Machine learning personalization
- Anomaly detection alerts
- Custom insights engine
- Report builder

### Phase 16 - Health Integration
- Fitness tracker integration
- Wearable device support
- Calorie burn tracking
- Health app synchronization
- Nutritionist consultation (future)

### Phase 17 - Advanced AI
- Dietary restriction management
- Allergy alerts
- Natural language queries ("What did I spend on snacks?")
- Receipt OCR
- Batch image recognition

### Phase 18 - Enterprise Features
- Multi-institutional deployment
- Student information system (SIS) integration
- Canteen POS integration
- Campus card integration
- Analytics dashboards for institutions

### Phase 19 - Monetization
- Premium features
- Institutional licensing
- API monetization
- Sponsored content (healthy restaurants)
- Affiliate marketing

---

## 📝 Notes & Constraints

### Technology Constraints
- Backend must use FastAPI for consistency
- Database must be PostgreSQL
- Frontend must use React with Vite
- No external payment processors initially
- Vision API selection to be finalized

### Team Constraints
- Single full-stack developer
- Limited budget for third-party services
- GitHub Copilot available for assistance

### Timeline
- 26-week implementation plan
- 2-3 days per phase
- Phased rollout to minimize risk

### Data Constraints
- Seed data includes 100 users, 50 food items, 2000 purchases
- Sample nutrition data provided
- Must not delete existing working code during refactoring

---

## ✅ Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-10 | Team | Initial document |

---

## 📞 Contact & Questions

For questions about this document, contact the development team.

---

**Document Status**: APPROVED FOR PHASE 1-2 AUDIT AND IMPLEMENTATION
