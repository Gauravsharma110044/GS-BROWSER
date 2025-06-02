import { initializeApp, getApps } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';
import { getAnalytics } from 'firebase/analytics';

const firebaseConfig = {
  apiKey: "AIzaSyBoNgPJ8b9AKIfevsoqKJ6tccnPggXPDsU",
  authDomain: "gpt-7aca7.firebaseapp.com",
  projectId: "gpt-7aca7",
  storageBucket: "gpt-7aca7.firebasestorage.app",
  messagingSenderId: "70245986843",
  appId: "1:70245986843:web:c1d4fd0f7e3a318cadbebe",
  measurementId: "G-4D790X0TJ0"
};

// Initialize Firebase
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);
const analytics = typeof window !== 'undefined' ? getAnalytics(app) : null;

// Configure Google Auth Provider
const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  client_id: "70245986843-aasvvsat6mpd2dq68bnh5dig941rt0hc.apps.googleusercontent.com"
});

export { app, auth, db, storage, analytics, googleProvider }; 