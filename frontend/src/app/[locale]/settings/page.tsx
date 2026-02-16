'use client';

import {useTranslations} from 'next-intl';
import {useEffect, useState} from 'react';
import {authAPI} from '@/lib/api';

export default function SettingsPage() {
  const t = useTranslations('settings');
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    telegram_chat_id: '',
    preferred_language: 'en',
    timezone: 'UTC'
  });
  
  useEffect(() => {
    loadUser();
  }, []);
  
  const loadUser = async () => {
    try {
      const response = await authAPI.getMe();
      setUser(response.data);
      setFormData({
        telegram_chat_id: response.data.telegram_chat_id || '',
        preferred_language: response.data.preferred_language || 'en',
        timezone: response.data.timezone || 'UTC'
      });
    } catch (error) {
      console.error('Failed to load user:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await authAPI.updateMe(formData);
      alert(t('save') + ' successful!');
      loadUser();
    } catch (error) {
      console.error('Failed to update settings:', error);
      alert('Failed to update settings');
    }
  };
  
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p>Loading...</p>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">{t('title')}</h1>
      
      <form onSubmit={handleSubmit}>
        {/* Telegram */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">{t('telegram.title')}</h2>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">{t('telegram.chatId')}</label>
            <input
              type="text"
              value={formData.telegram_chat_id}
              onChange={(e) => setFormData({...formData, telegram_chat_id: e.target.value})}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder="123456789"
            />
            <p className="text-sm text-gray-600 mt-2">{t('telegram.instructions')}</p>
          </div>
          <div className={`inline-block px-3 py-1 rounded-full text-sm ${
            formData.telegram_chat_id ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'
          }`}>
            {formData.telegram_chat_id ? t('telegram.connected') : t('telegram.notConnected')}
          </div>
        </div>
        
        {/* Language */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">{t('language.title')}</h2>
          <select
            value={formData.preferred_language}
            onChange={(e) => setFormData({...formData, preferred_language: e.target.value})}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="en">English</option>
            <option value="ko">한국어</option>
            <option value="ja">日本語</option>
            <option value="zh">中文</option>
            <option value="hi">हिन्दी</option>
            <option value="fr">Français</option>
            <option value="es">Español</option>
            <option value="ms">Bahasa Melayu</option>
            <option value="vi">Tiếng Việt</option>
          </select>
        </div>
        
        {/* Timezone */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">{t('timezone.title')}</h2>
          <select
            value={formData.timezone}
            onChange={(e) => setFormData({...formData, timezone: e.target.value})}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="UTC">UTC</option>
            <option value="America/New_York">Eastern Time (US)</option>
            <option value="America/Chicago">Central Time (US)</option>
            <option value="America/Los_Angeles">Pacific Time (US)</option>
            <option value="Europe/London">London</option>
            <option value="Europe/Paris">Paris</option>
            <option value="Asia/Tokyo">Tokyo</option>
            <option value="Asia/Seoul">Seoul</option>
            <option value="Asia/Shanghai">Shanghai</option>
            <option value="Asia/Kolkata">India</option>
          </select>
        </div>
        
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700"
        >
          {t('save')}
        </button>
      </form>
    </div>
  );
}
