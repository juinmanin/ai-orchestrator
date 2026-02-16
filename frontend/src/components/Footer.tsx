'use client';

import {useTranslations} from 'next-intl';
import {Link} from '@/i18n/routing';

export default function Footer() {
  const t = useTranslations('footer');
  
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-2xl font-bold mb-4">Open Crow</h3>
            <p className="text-gray-400">
              AI Quota Orchestrator - Never waste your AI quotas
            </p>
          </div>
          
          <div>
            <h4 className="font-bold mb-4">Links</h4>
            <div className="flex flex-col space-y-2">
              <Link href="/" className="text-gray-400 hover:text-white">{t('terms')}</Link>
              <Link href="/" className="text-gray-400 hover:text-white">{t('privacy')}</Link>
              <Link href="/" className="text-gray-400 hover:text-white">{t('contact')}</Link>
            </div>
          </div>
          
          <div>
            <h4 className="font-bold mb-4">Domain</h4>
            <p className="text-gray-400">open-crow.com</p>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>{t('copyright')}</p>
        </div>
      </div>
    </footer>
  );
}
