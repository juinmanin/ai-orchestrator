# Quick Start Guide

## For Development

### Backend Only
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Access at: http://localhost:8000/docs

### Frontend Only
```bash
cd frontend
npm install
npm run dev
```

Access at: http://localhost:3000

### Telegram Bot Only
```bash
cd telegram-bot
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="your-token"
export API_BASE_URL="http://localhost:8000"
python -m bot.main
```

## For Production

### Quick Deploy with Docker
```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your values

# 2. Start all services
docker-compose up -d

# 3. Check logs
docker-compose logs -f

# 4. Stop services
docker-compose down
```

### Environment Variables Required
- `ENCRYPTION_KEY`: 32+ character random string for API key encryption
- `JWT_SECRET`: Random string for JWT token signing
- `TELEGRAM_BOT_TOKEN`: From @BotFather on Telegram

## Testing the API

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Add Platform Account
```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "platform_id": "openai_free",
    "api_key": "your-api-key",
    "account_identifier": "your-email@example.com"
  }'
```

### Get Dashboard
```bash
curl http://localhost:8000/api/quota/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Important Files

### Backend
- `backend/app/main.py` - FastAPI app entry point
- `backend/app/config.py` - Configuration settings
- `backend/app/routers/` - API endpoints
- `backend/app/services/` - Business logic
- `backend/app/models/` - Database models
- `backend/app/data/platform_quotas.json` - Platform definitions

### Frontend
- `frontend/src/app/[locale]/page.tsx` - Landing page
- `frontend/src/app/[locale]/dashboard/page.tsx` - Dashboard
- `frontend/src/components/` - Reusable components
- `frontend/messages/` - Translations (9 languages)
- `frontend/src/lib/api.ts` - API client

### Telegram Bot
- `telegram-bot/bot/main.py` - Bot entry point
- `telegram-bot/bot/handlers.py` - Command handlers
- `telegram-bot/bot/scheduler.py` - Automated notifications
- `telegram-bot/bot/messages/` - Multi-language messages

## Common Issues

### Backend won't start
- Check if port 8000 is available
- Ensure all dependencies are installed
- Create `backend/data/` directory
- Verify environment variables

### Frontend build fails
- Run `npm install` again
- Check Node.js version (need v18+)
- Clear `.next` folder and rebuild

### Telegram bot not responding
- Verify TELEGRAM_BOT_TOKEN is correct
- Check bot username is unique
- Ensure API_BASE_URL points to backend

### Docker Compose issues
- Check Docker and Docker Compose versions
- Ensure ports 80, 443, 3000, 8000 are available
- Review logs: `docker-compose logs`

## Next Steps

1. **Configure SSL**: Follow README.md for Let's Encrypt setup
2. **Add More Platforms**: Edit `backend/app/data/platform_quotas.json`
3. **Customize Notifications**: Modify scheduler intervals in `telegram-bot/bot/scheduler.py`
4. **Enhance UI**: Customize Tailwind theme in `frontend/tailwind.config.ts`
5. **Add Tests**: Create tests in `backend/app/tests/`

## Support

For issues or questions:
- GitHub Issues: https://github.com/juinmanin/ai-orchestrator/issues
- Documentation: See README.md
