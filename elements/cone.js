class Cone {
    constructor(tip, baseCenter, baseRadius, numberOfSegmentsLengthwise, numberOfSegmentsCircumferential) {
        this.triangles = [];
        this.axis = new THREE.Vector3().subVectors(tip, baseCenter);
        this.lengthSegment = this.axis.clone().multiplyScalar(-1.0 / numberOfSegmentsLengthwise);
        console.log(`axis: ${JSON.stringify(this.axis)}`);
        console.log(`lengthSegment: ${JSON.stringify(this.lengthSegment)}`);
        
        for(let l = 0; l < numberOfSegmentsLengthwise; l++) {
            let segmentTip = tip
                .clone()
                .add(this.lengthSegment.clone().multiplyScalar(l));
            console.log(`segmentTip: ${JSON.stringify(segmentTip)}`);
            let segmentBase = tip
                .clone()
                .add(this.lengthSegment.clone().multiplyScalar(l + 1));
            console.log(`segmentBase: ${JSON.stringify(segmentBase)}`);
            for(let c = 0; c < numberOfSegmentsCircumferential; c++) {
                let segmentTipRadius = baseRadius
                    .clone()
                    .multiplyScalar(l / numberOfSegmentsLengthwise);
                let segmentBaseRadius = baseRadius
                    .clone()
                    .multiplyScalar((l + 1) / numberOfSegmentsLengthwise);
                let segmentTipRadius1 = segmentTipRadius
                    .clone()
                    .applyAxisAngle(
                        this.axis, 
                        c / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                let segmentTipRadius2 = segmentTipRadius
                    .clone()
                    .applyAxisAngle(
                        this.axis, 
                        (c + 1) / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                let segmentBaseRadius1 = segmentBaseRadius
                    .clone()
                    .applyAxisAngle(
                        this.axis, 
                        c / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                let segmentBaseRadius2 = segmentBaseRadius
                    .clone()
                    .applyAxisAngle(
                        this.axis, 
                        (c + 1) / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                let p0 = segmentTip.clone().add(segmentTipRadius1);
                let p1 = segmentBase.clone().add(segmentBaseRadius1);
                let p2 = segmentBase.clone().add(segmentBaseRadius2);
                this.triangles.push(new Triangle(
                    p0.toArray(),
                    p1.toArray(),
                    p2.toArray()
                ));
                if(l > 0) {
                    let p3 = segmentTip.clone().add(segmentTipRadius1);
                    let p4 = segmentBase.clone().add(segmentBaseRadius2);
                    let p5 = segmentTip.clone().add(segmentTipRadius2);
                    this.triangles.push(new Triangle(
                        p3.toArray(),
                        p4.toArray(),
                        p5.toArray()
                    ));
                }
            }
        }

        this.lines = this.triangles.map(t => t.lines);
        this.faces = this.triangles.map(t => t.face);
    }
}