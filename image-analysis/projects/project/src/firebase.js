// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth} from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCii06mLBdZXR4wCWAuPurxxVsi_99Zz-k",
  authDomain: "netflix-4918b.firebaseapp.com",
  projectId: "netflix-4918b",
  storageBucket: "netflix-4918b.appspot.com",
  messagingSenderId: "1045901490991",
  appId: "1:1045901490991:web:f3f04e36bb1c104b7b3fda",
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app)