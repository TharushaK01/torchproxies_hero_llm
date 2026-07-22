create table messages (
  id uuid default gen_random_uuid() primary key,
  session_id text not null,
  role text not null,
  content text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);