import { useEffect, useState } from "react";
import type { TaskRead } from "../../../entities/task";
import { useGetPresignedUrlForGetFromS3Query } from "../api/api";
import { skipToken } from "@reduxjs/toolkit/query";

export const Card = (props: TaskRead) => {
    // const [imageUrl, setImageURL] = useState<string | undefined>(undefined)
    const { 
        data: presignedUrlData
    } = useGetPresignedUrlForGetFromS3Query(
        `${props.file_id}.${props.file_extension}`, 
        {skip: !props.file_id})

    // const getImageFromS3 = async ()  => {
    //     try {
    //         if (presignedUrlData) {
    //             const response = await fetch(presignedUrlData)
    //             const url = await respo
    //         }
    //     } catch(err) {
    //         console.log(err)
    //     }
    // }
    // useEffect(() => {
    //     getImageFromS3()
    // }, [presignedUrlData])

    return (
        <div>
            <img src={presignedUrlData} />
        </div>
    )
}
