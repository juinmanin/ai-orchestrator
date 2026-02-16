'use client';

import {useRouter, usePathname} from '@/i18n/routing';
import {useParams} from 'next/navigation';

const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'ko', name: '한국어' },
  { code: 'ja', name: '日本語' },
  { code: 'zh', name: '中文' },
  { code: 'hi', name: 'हिन्दी' },
  { code: 'fr', name: 'Français' },
  { code: 'es', name: 'Español' },
  { code: 'ms', name: 'Bahasa Melayu' },
  { code: 'vi', name: 'Tiếng Việt' },
];

export default function LanguageSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const params = useParams();
  
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newLocale = e.target.value;
    router.replace(pathname, {locale: newLocale});
  };
  
  return (
    <select
      onChange={handleChange}
      value={params.locale as string}
      className="border border-gray-300 rounded px-2 py-1 text-sm"
    >
      {LANGUAGES.map((lang) => (
        <option key={lang.code} value={lang.code}>
          {lang.name}
        </option>
      ))}
    </select>
  );
}
