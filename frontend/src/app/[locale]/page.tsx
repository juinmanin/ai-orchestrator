import {useTranslations} from 'next-intl';
import {Link} from '@/i18n/routing';

export default function HomePage() {
  const t = useTranslations();
  
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">{t('hero.title')}</h1>
          <p className="text-xl mb-8">{t('hero.subtitle')}</p>
          <div className="flex gap-4 justify-center">
            <Link href="/dashboard" className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50">
              {t('hero.cta')}
            </Link>
            <a href="#features" className="border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700">
              {t('hero.learnMore')}
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-4">{t('features.title')}</h2>
          <p className="text-xl text-center text-gray-600 mb-12">{t('features.subtitle')}</p>
          
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard icon="📊" title={t('features.dashboard.title')} description={t('features.dashboard.description')} />
            <FeatureCard icon="🤖" title={t('features.telegram.title')} description={t('features.telegram.description')} />
            <FeatureCard icon="🧠" title={t('features.smart.title')} description={t('features.smart.description')} />
            <FeatureCard icon="🔒" title={t('features.secure.title')} description={t('features.secure.description')} />
            <FeatureCard icon="🌍" title={t('features.multilingual.title')} description={t('features.multilingual.description')} />
            <FeatureCard icon="📋" title={t('features.guides.title')} description={t('features.guides.description')} />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-4">{t('howItWorks.title')}</h2>
          <p className="text-xl text-center text-gray-600 mb-12">{t('howItWorks.subtitle')}</p>
          
          <div className="grid md:grid-cols-4 gap-8">
            <StepCard number="1" title={t('howItWorks.step1.title')} description={t('howItWorks.step1.description')} />
            <StepCard number="2" title={t('howItWorks.step2.title')} description={t('howItWorks.step2.description')} />
            <StepCard number="3" title={t('howItWorks.step3.title')} description={t('howItWorks.step3.description')} />
            <StepCard number="4" title={t('howItWorks.step4.title')} description={t('howItWorks.step4.description')} />
          </div>
        </div>
      </section>

      {/* Platforms Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-4">{t('platforms.title')}</h2>
          <p className="text-xl text-center text-gray-600 mb-12">{t('platforms.subtitle')}</p>
          
          <div className="flex flex-wrap justify-center gap-8 mb-8">
            <PlatformIcon name="ChatGPT" icon="🤖" />
            <PlatformIcon name="Gemini" icon="💎" />
            <PlatformIcon name="Claude" icon="🧠" />
            <PlatformIcon name="Leonardo AI" icon="🎨" />
            <PlatformIcon name="Hugging Face" icon="🤗" />
            <PlatformIcon name="Cohere" icon="🔷" />
          </div>
          
          <p className="text-center text-gray-600">{t('platforms.more')}</p>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="bg-gray-50 py-20">
        <div className="container mx-auto px-4 max-w-3xl">
          <h2 className="text-4xl font-bold text-center mb-12">{t('faq.title')}</h2>
          
          <div className="space-y-6">
            <FAQItem question={t('faq.q1.question')} answer={t('faq.q1.answer')} />
            <FAQItem question={t('faq.q2.question')} answer={t('faq.q2.answer')} />
            <FAQItem question={t('faq.q3.question')} answer={t('faq.q3.answer')} />
            <FAQItem question={t('faq.q4.question')} answer={t('faq.q4.answer')} />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">{t('hero.title')}</h2>
          <Link href="/dashboard" className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50">
            {t('hero.cta')}
          </Link>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function StepCard({ number, title, description }: { number: string; title: string; description: string }) {
  return (
    <div className="text-center">
      <div className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
        {number}
      </div>
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function PlatformIcon({ name, icon }: { name: string; icon: string }) {
  return (
    <div className="text-center">
      <div className="text-5xl mb-2">{icon}</div>
      <p className="font-semibold">{name}</p>
    </div>
  );
}

function FAQItem({ question, answer }: { question: string; answer: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-3">{question}</h3>
      <p className="text-gray-600">{answer}</p>
    </div>
  );
}
