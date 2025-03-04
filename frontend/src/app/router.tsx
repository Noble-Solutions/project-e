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
import { AddStudent, MainList, SingleClassroom } from '../features/singleClassroom';
import { SingleVariant, TaskList, VariantResults } from '../features/singleVariant';
import { SingleStudent } from '../features/singleClassroom';
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
                            {
                                path: 'single/:id',
                                element: <SingleVariant/>,
                                children: [
                                    {
                                        path: 'main-widget/:task_id?',
                                        element: <TaskList />
                                    },
                                    {
                                        path: 'variant-results',
                                        element: <VariantResults/>
                                    }
                                ]
                            }
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
                            {
                                path: 'single/:id',
                                element: <SingleClassroom/>,
                                children: [
                                    {
                                        path: 'main-widget',
                                        element: <MainList />
                                    },

                                ]

                            }
                        ]
                    }
                ]
            },
    



            // TEACHER ROUTES
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
                            },
                            {
                                path: 'single/:id',
                                element: <SingleClassroom/>,
                                children: [
                                    {
                                        path: 'main-widget',
                                        element: <MainList />
                                    },
                                    {
                                        path: 'add-student/',
                                        element: <AddStudent/>
                                    },
                                    {
                                        path: 'performance/:student_id',
                                        element: <SingleStudent/>
                                    },
                                ]

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
                            },
                            {
                                path: 'single/:id',
                                element: <SingleVariant/>,
                                children: [
                                    {
                                        path: 'main-widget/:task_id?',
                                        element: <TaskList />
                                    },
                                ]
                            }
                        ]
                    },
                    {
                        path: 'tasks/',
                        element: <Tasks/>,
                        children: [
                            {
                                path: 'list/:variant_id?',
                                element: <TasksList/>
                            },
                            {
                                path: 'create/:variant_id?',
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