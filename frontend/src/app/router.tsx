import { createBrowserRouter } from 'react-router-dom';
import { PageNotFoundError } from '../shared/ui/PageNotFoundError';
import { Auth } from '../pages/auth';
import { Root } from '../pages/root';
import { VariantList } from '../widgets/variantList';
import { ClassList } from '../widgets/classList';
export const router = createBrowserRouter([
    {
        path: '/student/',
        element: <Root/>,
        errorElement: <PageNotFoundError/>,
        children: [
            {
                path: 'variants/',
                element: <VariantList/>,
            },
            {
                path: 'classes/',
                element: <ClassList/>
            }
        ]
    },
    {
        path: '/teacher',
        element: <PageNotFoundError/>,
        children: [
            {
                path: 'classes/',
                element: <ClassList/>
            },
            {
                path: 'variants/',
                element: <VariantList/>
            },
            {
                path: 'tasks/',
                element: <PageNotFoundError/>
            }
        ]
    },
    {
        path: "/auth/:authType/",
        element: <Auth/>,
        errorElement: <PageNotFoundError/>,
        loader: ({ params }) => {
            if (params.authType !== 'login' && params.authType !== 'register') {
                throw new Response("Not Found", { status: 404 });
            }
            return null
        }
    }
])