import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://hkeheukewxsvaarxaket.supabase.co',
  process.env.SUPABASE_SERVICE_ROLE_KEY || ''
);

export { supabase };
