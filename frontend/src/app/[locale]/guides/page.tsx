'use client';

import {useTranslations} from 'next-intl';
import {useEffect, useState} from 'react';
import {guidesAPI} from '@/lib/api';

export default function GuidesPage() {
  const t = useTranslations('guides');
  const [platforms, setPlatforms] = useState<any[]>([]);
  const [selectedPlatform, setSelectedPlatform] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadPlatforms();
  }, []);
  
  const loadPlatforms = async () => {
    try {
      const response = await guidesAPI.list();
      setPlatforms(response.data);
    } catch (error) {
      console.error('Failed to load platforms:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const loadGuide = async (platformId: string) => {
    try {
      const response = await guidesAPI.get(platformId);
      setSelectedPlatform(response.data);
    } catch (error) {
      console.error('Failed to load guide:', error);
    }
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">{t('title')}</h1>
      <p className="text-gray-600 mb-8">{t('subtitle')}</p>
      
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="grid md:grid-cols-3 gap-8">
          {/* Platform List */}
          <div className="md:col-span-1">
            <h2 className="text-xl font-bold mb-4">{t('selectPlatform')}</h2>
            <div className="space-y-2">
              {platforms.map((platform) => (
                <button
                  key={platform.platform_id}
                  onClick={() => loadGuide(platform.platform_id)}
                  className={`w-full text-left p-4 rounded-lg border ${
                    selectedPlatform?.platform_id === platform.platform_id
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{platform.icon}</span>
                    <div>
                      <h3 className="font-bold">{platform.platform_name}</h3>
                      <p className="text-sm text-gray-600">{platform.description}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
          
          {/* Guide Details */}
          <div className="md:col-span-2">
            {selectedPlatform ? (
              <div>
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                  <div className="flex items-center gap-3 mb-4">
                    <span className="text-4xl">{selectedPlatform.icon}</span>
                    <div>
                      <h2 className="text-2xl font-bold">{selectedPlatform.platform_name}</h2>
                      <p className="text-gray-600">{selectedPlatform.description}</p>
                    </div>
                  </div>
                  
                  <div className="flex gap-4">
                    <a
                      href={selectedPlatform.signup_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                    >
                      {t('visit')}
                    </a>
                    {selectedPlatform.api_docs_url && (
                      <a
                        href={selectedPlatform.api_docs_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
                      >
                        {t('apiDocs')}
                      </a>
                    )}
                  </div>
                </div>
                
                {/* Steps */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                  <h3 className="text-xl font-bold mb-4">{t('steps')}</h3>
                  <div className="space-y-4">
                    {selectedPlatform.steps?.map((step: any) => (
                      <div key={step.step} className="flex gap-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                          {step.step}
                        </div>
                        <div className="flex-1">
                          <h4 className="font-bold mb-1">{step.title}</h4>
                          <p className="text-gray-600 mb-2">{step.description}</p>
                          {step.tips && step.tips.length > 0 && (
                            <ul className="list-disc list-inside text-sm text-gray-500">
                              {step.tips.map((tip: string, i: number) => (
                                <li key={i}>{tip}</li>
                              ))}
                            </ul>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                {/* Platform Tips */}
                {selectedPlatform.platform_tips && selectedPlatform.platform_tips.length > 0 && (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                    <h3 className="text-xl font-bold mb-4">{t('tips')}</h3>
                    <ul className="list-disc list-inside space-y-2">
                      {selectedPlatform.platform_tips.map((tip: string, i: number) => (
                        <li key={i} className="text-gray-700">{tip}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-gray-50 rounded-lg p-12 text-center text-gray-600">
                <p>{t('selectPlatform')}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
