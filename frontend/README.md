# Frontend — Doctor Dashboard

## Goal
Real-time dashboard showing patients, AI risk scores, explainability, and hospital recommendations.

## Setup
```bash
npx create-react-app . 
# or: npm create vite@latest . -- --template react
npm install axios chart.js react-chartjs-2 tailwindcss
```

## Key Screens
1. **Patient List** — color-coded by risk (🔴 Critical / 🟡 Urgent / 🟢 Stable)
2. **Patient Detail** — vitals + AI explanation (why this risk score)
3. **Hospital Map/List** — nearby hospitals with live bed availability
4. **Alerts Panel** — real-time incoming emergency alerts

## Next Steps
1. Build wireframes in Figma first
2. Set up React project + Tailwind
3. Connect to backend APIs
4. Add WebSocket client for live alerts
