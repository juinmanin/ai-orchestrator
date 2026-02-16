'use client';

import {useTranslations} from 'next-intl';
import {useEffect, useState} from 'react';
import {accountsAPI, guidesAPI} from '@/lib/api';

export default function AccountsPage() {
  const t = useTranslations('accounts');
  const [accounts, setAccounts] = useState<any[]>([]);
  const [platforms, setPlatforms] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  
  useEffect(() => {
    loadData();
  }, []);
  
  const loadData = async () => {
    try {
      const [accountsRes, platformsRes] = await Promise.all([
        accountsAPI.list(),
        guidesAPI.list()
      ]);
      setAccounts(accountsRes.data);
      setPlatforms(platformsRes.data);
    } catch (error) {
      console.error('Failed to load accounts:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this account?')) return;
    
    try {
      await accountsAPI.delete(id);
      loadData();
    } catch (error) {
      console.error('Failed to delete account:', error);
    }
  };
  
  const handleVerify = async (id: number) => {
    try {
      await accountsAPI.verify(id);
      loadData();
    } catch (error) {
      console.error('Failed to verify account:', error);
    }
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
        >
          {t('addAccount')}
        </button>
      </div>
      
      {loading ? (
        <p>Loading...</p>
      ) : accounts.length === 0 ? (
        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <p className="text-gray-600 mb-4">No accounts connected yet.</p>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            {t('addAccount')}
          </button>
        </div>
      ) : (
        <div className="grid gap-4">
          {accounts.map((account) => (
            <div key={account.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-xl font-bold mb-1">{account.platform_id}</h3>
                  <p className="text-gray-600 text-sm mb-2">API Key: {account.api_key_preview}</p>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm ${
                    account.is_verified ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'
                  }`}>
                    {account.is_verified ? t('verified') : t('notVerified')}
                  </span>
                </div>
                <div className="flex gap-2">
                  {!account.is_verified && (
                    <button
                      onClick={() => handleVerify(account.id)}
                      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                    >
                      {t('verify')}
                    </button>
                  )}
                  <button
                    onClick={() => handleDelete(account.id)}
                    className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                  >
                    {t('delete')}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {showModal && (
        <AddAccountModal
          platforms={platforms}
          onClose={() => setShowModal(false)}
          onSuccess={() => {
            setShowModal(false);
            loadData();
          }}
        />
      )}
    </div>
  );
}

function AddAccountModal({ platforms, onClose, onSuccess }: any) {
  const t = useTranslations('accounts');
  const [formData, setFormData] = useState({
    platform_id: '',
    api_key: '',
    account_identifier: ''
  });
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await accountsAPI.create(formData);
      onSuccess();
    } catch (error) {
      console.error('Failed to add account:', error);
      alert('Failed to add account');
    }
  };
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">{t('modalTitle')}</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">{t('selectPlatform')}</label>
            <select
              value={formData.platform_id}
              onChange={(e) => setFormData({...formData, platform_id: e.target.value})}
              className="w-full border border-gray-300 rounded px-3 py-2"
              required
            >
              <option value="">Select...</option>
              {platforms.map((p: any) => (
                <option key={p.platform_id} value={p.platform_id}>
                  {p.platform_name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">{t('apiKey')}</label>
            <input
              type="password"
              value={formData.api_key}
              onChange={(e) => setFormData({...formData, api_key: e.target.value})}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder={t('apiKeyPlaceholder')}
              required
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-gray-700 mb-2">{t('accountIdentifier')}</label>
            <input
              type="text"
              value={formData.account_identifier}
              onChange={(e) => setFormData({...formData, account_identifier: e.target.value})}
              className="w-full border border-gray-300 rounded px-3 py-2"
              placeholder={t('accountIdentifierPlaceholder')}
            />
          </div>
          
          <div className="flex gap-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
            >
              {t('cancel')}
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {t('save')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
