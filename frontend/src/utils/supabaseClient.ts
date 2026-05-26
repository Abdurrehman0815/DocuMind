import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://mvfpjxwhbcvaofhuiryv.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12ZnBqeHdoYmN2YW9maHVpcnl2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3Nzc0NTEsImV4cCI6MjA5NTM1MzQ1MX0.doic3X-ZPEf2FF2TlTenQRzoQnJotwOWK83HLIITIbk'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
