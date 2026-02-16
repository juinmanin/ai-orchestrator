'use client';

import {useTranslations} from 'next-intl';
import {Link} from '@/i18n/routing';
import LanguageSwitcher from './LanguageSwitcher';

export default function Header() {
  const t = useTranslations('nav');
  
  return (
    <header className="bg-white shadow-sm">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-blue-600">
            Open Crow
          </Link>
          
          <div className="hidden md:flex items-center space-x-6">
            <Link href="/" className="text-gray-700 hover:text-blue-600">
              {t('home')}
            </Link>
            <Link href="/dashboard" className="text-gray-700 hover:text-blue-600">
              {t('dashboard')}
            </Link>
            <Link href="/accounts" className="text-gray-700 hover:text-blue-600">
              {t('accounts')}
            </Link>
            <Link href="/guides" className="text-gray-700 hover:text-blue-600">
              {t('guides')}
            </Link>
            <Link href="/settings" className="text-gray-700 hover:text-blue-600">
              {t('settings')}
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <LanguageSwitcher />
            <Link href="/login" className="text-gray-700 hover:text-blue-600">
              {t('login')}
            </Link>
            <Link href="/register" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              {t('register')}
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}
