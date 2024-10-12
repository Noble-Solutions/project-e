import { createBrowserRouter } from 'react-router-dom';
import { PageNotFoundError } from '../shared/ui/PageNotFoundError';
import { Auth } from '../pages/auth';
import { Root } from '../pages/root';
import { VariantList } from '../features/variantList';
import { ClassRoomsList } from '../features/classroomsList';
import { VariantCreateForm } from '../features/variantCreate';
import { Variants } from '../widgets/variants';
import { Classrooms } from '../widgets/classrooms';
import { ClassRoomsCreateForm } from '../features/classRoomCreate';
import { Tasks } from '../widgets/tasks';
import { TasksList } from '../features/taskList';
import { TaskCreateForm } from '../features/taskCreate';
import { App } from './App';
export const router = createBrowserRouter([
    {
        path: '/',
        element: <App/>,
        errorElement: <PageNotFoundError/>,
        children: [
            {
                path: 'student/',
                element: <Root/>,
                errorElement: <PageNotFoundError/>,
                children: [
                    {
                        path: 'variants/',
                        element: <Variants/>,
                        children: [
                            {
                                path: 'list/',
                                element: <VariantList/>
                            },
                        ]
                    },
                    {
                        path: 'classes/',
                        element: <Classrooms/>,
                        children: [
                            {
                                path: 'list/',
                                element: <ClassRoomsList/>
                            },
                        ]
                    }
                ]
            },
            {
                path: 'teacher/',
                element: <Root/>,
                errorElement: <PageNotFoundError/>,
                children: [
                    {
                        path: 'classes/',
                        element: <Classrooms/>,
                        children: [
                            {
                                path: 'list/',
                                element: <ClassRoomsList/>
                            },
                            {
                                path: 'create/',
                                element: <ClassRoomsCreateForm/>
                            }
                        ]
                    },
                    {
                        path: 'variants/',
                        element: <Variants/>,
                        children: [
                            {
                                path: 'list/',
                                element: <VariantList/>
                            },
                            {
                                path: 'create/',
                                element: <VariantCreateForm/>
                            }
                        ]
                    },
                    {
                        path: 'tasks/',
                        element: <Tasks/>,
                        children: [
                            {
                                path: 'list/',
                                element: <TasksList/>
                            },
                            {
                                path: 'create/',
                                element: <TaskCreateForm/>
                            }
                        ]
                    }
                ]
            },
            
        ]
    },
    {
        path: "auth/:authType/",
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