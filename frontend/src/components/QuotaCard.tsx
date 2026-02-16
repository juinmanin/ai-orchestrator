'use client';

interface QuotaCardProps {
  platformName: string;
  icon: string;
  quotas: Array<{
    quota_type: string;
    used_quota: number;
    total_quota: number;
    usage_percentage: number;
    reset_at: string;
  }>;
  urgencyScore: number;
  recommendation: string;
}

export default function QuotaCard({ platformName, icon, quotas, urgencyScore, recommendation }: QuotaCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{icon}</span>
          <h3 className="text-xl font-bold">{platformName}</h3>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
          urgencyScore > 70 ? 'bg-red-100 text-red-600' :
          urgencyScore > 30 ? 'bg-yellow-100 text-yellow-600' :
          'bg-green-100 text-green-600'
        }`}>
          {recommendation}
        </div>
      </div>
      
      <div className="space-y-3">
        {quotas.map((quota, index) => (
          <div key={index}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">{quota.quota_type}</span>
              <span className="font-semibold">
                {quota.used_quota.toFixed(0)}/{quota.total_quota.toFixed(0)}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${
                  quota.usage_percentage > 90 ? 'bg-red-500' :
                  quota.usage_percentage > 70 ? 'bg-yellow-500' :
                  'bg-green-500'
                }`}
                style={{ width: `${Math.min(quota.usage_percentage, 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
