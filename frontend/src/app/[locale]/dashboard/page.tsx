'use client';

import {useTranslations} from 'next-intl';
import {useEffect, useState} from 'react';
import {quotaAPI} from '@/lib/api';
import QuotaCard from '@/components/QuotaCard';

export default function DashboardPage() {
  const t = useTranslations('dashboard');
  const [dashboard, setDashboard] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadDashboard();
  }, []);
  
  const loadDashboard = async () => {
    try {
      const response = await quotaAPI.dashboard();
      setDashboard(response.data);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p className="text-center">{t('loading')}</p>
      </div>
    );
  }
  
  if (!dashboard || dashboard.connected_accounts === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">{t('title')}</h1>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <p className="text-yellow-800">{t('noAccounts')}</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">{t('title')}</h1>
      
      {/* Overview Stats */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-gray-600 mb-2">{t('totalPlatforms')}</h3>
          <p className="text-3xl font-bold">{dashboard.total_platforms}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-gray-600 mb-2">{t('connectedAccounts')}</h3>
          <p className="text-3xl font-bold">{dashboard.connected_accounts}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-gray-600 mb-2">{t('overallUsage')}</h3>
          <p className="text-3xl font-bold">{dashboard.total_quota_usage_percentage.toFixed(1)}%</p>
        </div>
      </div>
      
      {/* Platform Cards */}
      <h2 className="text-2xl font-bold mb-4">Your Platforms</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {dashboard.platforms.map((platform: any) => (
          <QuotaCard
            key={platform.platform_id}
            platformName={platform.platform_name}
            icon={platform.platform_id === 'openai_free' ? '🤖' : 
                  platform.platform_id === 'gemini_free' ? '💎' :
                  platform.platform_id === 'claude_free' ? '🧠' :
                  platform.platform_id === 'leonardo_free' ? '🎨' :
                  platform.platform_id === 'huggingface_free' ? '🤗' : '🔷'}
            quotas={platform.quotas}
            urgencyScore={platform.urgency_score}
            recommendation={platform.recommendation}
          />
        ))}
      </div>
    </div>
  );
}
